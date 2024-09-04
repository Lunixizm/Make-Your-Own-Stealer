import os
from PIL import ImageGrab

# Define the Windows Temp directory path
temp_dir = r"C:\Windows\Temp"

def screen():
    # Capture the screenshot
    sss = ImageGrab.grab()
    
    # Define the path where the screenshot will be saved
    temp_path = os.path.join(temp_dir, "ss.png")
    
    # Save the screenshot
    sss.save(temp_path)
    
    # Inform the user about the saved screenshot
    print(f"Screenshot saved to {temp_path}")

# Execute the function
screen()
