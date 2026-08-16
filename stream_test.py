import os
import time
import json
import pathlib
import subprocess
from DrissionPage import ChromiumOptions, ChromiumPage

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
TARGET_URL = os.getenv("TARGET_URL", "https://w2.sportsonlinee.click/channels/hd/hd1.php")
STREAM_KEY = os.getenv("STREAM_KEY", "YOUR_TEST_STREAM_KEY_HERE")
RES_W, RES_H = 1920, 1080
BITRATE = 3000

# ==========================================
# 🛠️ OBS STUDIO SETUP FUNCTION
# ==========================================
def setup_obs_config():
    print("[*] OBS Configuration set kar raha hoon...")
    home = str(pathlib.Path.home())
    obs_dir = os.path.join(home, '.config', 'obs-studio')
    prof_dir = os.path.join(obs_dir, 'basic', 'profiles', 'Untitled')
    scene_dir = os.path.join(obs_dir, 'basic', 'scenes')

    os.makedirs(prof_dir, exist_ok=True)
    os.makedirs(scene_dir, exist_ok=True)

    # 1. global.ini
    global_ini = "[General]\nLicenseAccepted=true\n[BasicWindow]\nShowAutoConfig=false\nWarned=true\n[OBSWebSocket]\nServerEnabled=true\nServerPort=4455\nServerPassword=secret\n"
    with open(os.path.join(obs_dir, 'global.ini'), 'w') as f: f.write(global_ini)

    # 2. basic.ini
    basic_ini = f"[General]\nName=Untitled\n[Video]\nBaseCX={RES_W}\nBaseCY={RES_H}\nOutputCX={RES_W}\nOutputCY={RES_H}\nFPSCommon=30\n[Output]\nMode=Simple\n[SimpleOutput]\nVBitrate={BITRATE}\nStreamEncoder=x264\nx264Preset=ultrafast\nx264Settings=keyint=60 tune=zerolatency profile=main threads=4 rc-lookahead=0\n"
    with open(os.path.join(prof_dir, 'basic.ini'), 'w') as f: f.write(basic_ini)

    # 3. service.json (Stream Key)
    service_json = { "settings": { "server": "rtmp://vsu.okcdn.ru/input/", "key": STREAM_KEY }, "type": "rtmp_custom" }
    with open(os.path.join(prof_dir, 'service.json'), 'w') as f: json.dump(service_json, f, indent=2)

    # 4. Scene Setup (Screen Capture + Audio)
    scene_json = {
        "current_scene": "MainScene", "current_program_scene": "MainScene", "name": "Untitled",
        "scene_order": [{"name": "MainScene"}],
        "sources": [
            { "id": "xshm_input", "name": "Screen", "settings": { "show_cursor": False } },
            { "id": "pulse_output_capture", "name": "Audio", "settings": {} },
            { "id": "scene", "name": "MainScene", "settings": { "items": [ 
                {"name": "Screen", "id": 1, "visible": True}, 
                {"name": "Audio", "id": 2, "visible": True} 
            ]}}
        ]
    }
    with open(os.path.join(scene_dir, 'Untitled.json'), 'w') as f: json.dump(scene_json, f, indent=2)


# ==========================================
# 🚀 MAIN LAUNCHER
# ==========================================
def main():
    setup_obs_config()

    # 1. OBS ko background mein start karein aur automatically streaming ON karein
    print("[*] OBS Studio start kar raha hoon...")
    obs_process = subprocess.Popen(['obs', '--startstreaming', '--minimize-to-tray'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(10) # OBS ko open hone ka time dein

    print(f"[*] DrissionPage ke zariye {TARGET_URL} open kar raha hoon...")
    
    # 2. Browser Options (Full Screen, No Sandbox)
    co = ChromiumOptions()
    co.set_argument('--no-sandbox')
    co.set_argument('--start-fullscreen')
    co.set_argument('--autoplay-policy=no-user-gesture-required')
    
    # 3. Asli Chrome launch karein aur Link open karein
    page = ChromiumPage(addr_or_opts=co)
    page.get(TARGET_URL)

    print("[*] Website load ho chuki hai. Streaming jari hai...")
    print("[!] Testing mode: Script ab infinite loop mein chalta rahega. Rokne ke liye Action cancel karein.")

    # 4. Infinite Loop (Stream chalti rahegi)
    try:
        while True:
            time.sleep(60)
            print("[💓] Stream is running...")
    except KeyboardInterrupt:
        print("[*] Band kiya ja raha hai...")
    finally:
        page.quit()
        obs_process.kill()

if __name__ == "__main__":
    main()
