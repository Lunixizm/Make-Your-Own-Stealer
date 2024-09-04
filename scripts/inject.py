import ctypes
import sys
import os

def dll_inject(process_id, dll_path):
    # Required access rights for the target process
    process_access_rights = 0x1F0FFF
    kernel32 = ctypes.windll.kernel32

    # Open the target process using the provided process ID
    process_handle = kernel32.OpenProcess(process_access_rights, False, process_id)
    
    if not process_handle:
        print(f"Error opening process: {kernel32.GetLastError()}")
        return False

    # Allocate memory in the target process for the DLL path
    dll_path_bytes = dll_path.encode('utf-8')
    dll_path_len = len(dll_path_bytes) + 1
    alloc_mem = kernel32.VirtualAllocEx(process_handle, 0, dll_path_len, 0x1000 | 0x2000, 0x40)
    
    if not alloc_mem:
        print(f"Error allocating memory: {kernel32.GetLastError()}")
        kernel32.CloseHandle(process_handle)
        return False

    # Write the DLL path into the allocated memory
    written = ctypes.c_int(0)
    if not kernel32.WriteProcessMemory(process_handle, alloc_mem, dll_path_bytes, dll_path_len, ctypes.byref(written)):
        print(f"Error writing to process memory: {kernel32.GetLastError()}")
        kernel32.VirtualFreeEx(process_handle, alloc_mem, 0, 0x8000)
        kernel32.CloseHandle(process_handle)
        return False

    # Get the address of the LoadLibraryA function
    load_library_addr = kernel32.GetProcAddress(kernel32.GetModuleHandleA(b"kernel32.dll"), b"LoadLibraryA")
    if not load_library_addr:
        print(f"Error retrieving LoadLibraryA address: {kernel32.GetLastError()}")
        kernel32.VirtualFreeEx(process_handle, alloc_mem, 0, 0x8000)
        kernel32.CloseHandle(process_handle)
        return False

    # Create a remote thread to load the DLL
    thread_id = ctypes.c_ulong(0)
    if not kernel32.CreateRemoteThread(process_handle, None, 0, load_library_addr, alloc_mem, 0, ctypes.byref(thread_id)):
        print(f"Error creating remote thread: {kernel32.GetLastError()}")
        kernel32.VirtualFreeEx(process_handle, alloc_mem, 0, 0x8000)
        kernel32.CloseHandle(process_handle)
        return False

    # Clean up
    kernel32.VirtualFreeEx(process_handle, alloc_mem, 0, 0x8000)
    kernel32.CloseHandle(process_handle)
    print("DLL injected successfully!")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dll_inject.py <Process ID> <DLL Path>")
        sys.exit(1)
    
    process_id = int(sys.argv[1])
    dll_path = sys.argv[2]

    if not os.path.exists(dll_path):
        print("Invalid DLL path!")
        sys.exit(1)

    dll_inject(process_id, dll_path)
