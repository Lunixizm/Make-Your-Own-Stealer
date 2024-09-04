import os

def find_antivirus_folders(base_folder):
    antivirus_names = [
        "Avast", "AVG", "Bitdefender", "Kaspersky", "McAfee", "Norton", "Sophos",
        "ESET", "Malwarebytes", "Avira", "Panda", "Trend Micro", "F-Secure", "Comodo",
        "BullGuard", "360 Total Security", "Ad-Aware", "Dr.Web", "G-Data", "Vipre",
        "ClamWin", "ZoneAlarm", "Cylance", "Webroot", "Palo Alto Networks", "Symantec",
        "SentinelOne", "CrowdStrike", "Emsisoft", "HitmanPro", "Fortinet", "FireEye",
        "Zemana", "Windows Defender", "AhnLab", "VIPRE", "Zillya", "Rising", "K7",
        "Quick Heal", "Comodo", "AhnLab V3", "Arcabit", "Ikarus", "Kingsoft", "MicroWorld",
        "Ad-aware", "Rising Antivirus"
    ]
    
    # Known antivirus folder names and executable names
    known_folders = {
        "Kaspersky": ["Kaspersky Lab", "Kaspersky", "Kaspersky Lab"],
    }
    
    known_executables = {
        "Avast": ["avastui.exe"],
        "AVG": ["avgui.exe"],
        "Bitdefender": ["vsserv.exe"],
        "Kaspersky": ["avp.exe", "klvssbridge.exe"],  # Add other known executables if needed
        "McAfee": ["mcshield.exe"],
        "Norton": ["nortonsecurity.exe"],
        "Sophos": ["sophos.exe"],
        "ESET": ["egui.exe"],
        "Malwarebytes": ["mbam.exe"],
        "Avira": ["avguard.exe"],
        "Panda": ["pavsrvx86.exe"],
        "Trend Micro": ["tmc.exe"],
        "F-Secure": ["fsua.exe"],
        "Comodo": ["cfp.exe"],
        "BullGuard": ["bgsvc.exe"],
        "360 Total Security": ["360sd.exe"],
        "Ad-Aware": ["ad-aware.exe"],
        "Dr.Web": ["drweb.exe"],
        "G-Data": ["gdata.exe"],
        "Vipre": ["vipre.exe"],
        "ClamWin": ["clamscan.exe"],
        "ZoneAlarm": ["zlclient.exe"],
        "Cylance": ["cylance.exe"],
        "Webroot": ["wrsa.exe"],
        "Palo Alto Networks": ["traps.sys"],
        "Symantec": ["symantec.exe"],
        "SentinelOne": ["sentinelagent.exe"],
        "CrowdStrike": ["falcon-sensor.exe"],
        "Emsisoft": ["a2start.exe"],
        "HitmanPro": ["hitmanpro.exe"],
        "Fortinet": ["fortiagent.exe"],
        "FireEye": ["fireeye.exe"],
        "Zemana": ["zemana.exe"],
        "Windows Defender": ["MsMpEng.exe"],
        "AhnLab": ["ahnlab.exe"],
        "VIPRE": ["vipre.exe"],
        "Zillya": ["zillya.exe"],
        "Rising": ["rising.exe"],
        "K7": ["k7.exe"],
        "Quick Heal": ["quickheal.exe"],
        "Comodo": ["cfp.exe"],
        "AhnLab V3": ["v3.exe"],
        "Arcabit": ["arcabit.exe"],
        "Ikarus": ["ikarus.exe"],
        "Kingsoft": ["kingsoft.exe"],
        "MicroWorld": ["mwavscan.exe"],
        "Ad-aware": ["ad-aware.exe"],
        "Rising Antivirus": ["rising.exe"]
    }
    
    antivirus_folders_dict = {}

    # Walk through directories and check for known antivirus folders and executables
    for root, dirs, files in os.walk(base_folder):
        for folder in dirs:
            # Check if folder name matches any known antivirus folder names
            for antivirus_name, folder_names in known_folders.items():
                if any(folder_name.lower() in folder.lower() for folder_name in folder_names):
                    antivirus_folders_dict[antivirus_name] = os.path.join(root, folder)
        
        for file in files:
            # Check if file name matches any known antivirus executables
            for antivirus_name, exec_names in known_executables.items():
                if file.lower() in [exec_name.lower() for exec_name in exec_names]:
                    if antivirus_name not in antivirus_folders_dict:
                        antivirus_folders_dict[antivirus_name] = root
    
    return antivirus_folders_dict

antivirus_folders = find_antivirus_folders("C:\\Program Files")

if antivirus_folders:
    print("\nAntivirus found:\n")
    for antivirus_name, folder_path in antivirus_folders.items():
        print(f"{antivirus_name}: {folder_path}")
else:
    print("No antivirus programs found.")
