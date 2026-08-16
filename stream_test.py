import os
import time
import json
import pathlib
import subprocess
from DrissionPage import ChromiumOptions, ChromiumPage

# ==========================================
# 🔑 MULTI-STREAM KEY MANAGER
# ==========================================
STREAM_KEYS = {
    '1'   : '15254238731883_15281627925099_najspfkgne', 
    '1.1' : '15254260751979_15281671637611_2plrcfqzze', 
    '1.2' : '15254285524587_15281717840491_7e6qdknzsu',
    
    '2'   : '15254299352683_15281743071851_7dvz3h5d7q',
    '2.1' : '15254308986475_15281761618539_3xca7oij3u',
    '2.2' : '15254328122987_15281795566187_zjqa6bqzoq', 

    '3'   : '15254341885547_15281821059691_hhlpb5vicy', 
    '3.1' : '15254357089899_15281848322667_sxeexgvzl4', 
    '3.2' : '15254367510123_15281868180075_pc4jrytfgm',

    '4'   : '15255022345835_15283095800427_vwrupxzstm', 
    '4.1' : '15255038074475_15283122080363_ai5qqp2we4', 
    '4.2' : '15255045480043_15283135842923_tldl4bhmii',
    '4.3' : '15255208599147_15283449629291_abltofuc7m', 
    '4.4' : '15255217708651_15283466603115_bojrrqtlmu', 
    '4.5' : '15255227670123_15283486263915_jpntt54mve',

    '5'   : '15273689226859_15317451606635_d7zzy3c7qi', 
    '5.1' : '15273713933931_15317494860395_avj47smmim', 
    '5.2' : '15273722257003_15317510195819_6edjluvdqi',
    '5.3' : '15273739624043_15317541653099_ii4bxpvabe',
    '5.4' : '15273750175339_15317561707115_csel26ku5a', 
    '5.5' : '15273760071275_15317579467371_cnewcj54me',
    '5.6' : '15273767935595_15317595851371_3q43tk7tvm', 
    
    's1.1'  : '14204232736303_14846150314543_37jq4ryehq',
    's1.2'  : '14204288179759_14846247373359_tnsknmapva',
    's1.3'  : '14204319768111_14846302489135_sr4ht4ccwq',
    's1.4'  : '14204331957807_14846326147631_dji2acqcze',
    's1.5'  : '14204346572335_14846351641135_7gvns4o5ue',
    's1.6'  : '14204361252399_14846376479279_cjajhf4d3y',
    's1.7'  : '14204370492975_14846393649711_6fduhdqite',
    's1.8'  : '14204395527727_14846438017583_s2jlti7lsm',
    's1.9'  : '14204411387439_14846464887343_f5lxgcqj5y',
    's1.10' : '14204424691247_14846487562799_xmbvntt6wa',
    's2.1'  : '14204490948143_14846603495983_kzevn36tii',
    's2.10' : '14206184136239_14849618610735_ihnbx7hkoi'
}

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
TARGET_URL = os.getenv("TARGET_URL", "https://w2.sportsonlinee.click/channels/hd/hd1.php")
STREAM_ID = os.getenv("OKRU_STREAM_ID", "1")
ACTIVE_STREAM_KEY = STREAM_KEYS.get(STREAM_ID, STREAM_KEYS['1']) # Default to '1' if not found

RES_W, RES_H = 1920, 1080
BITRATE = 3000

# ==========================================
# 🛠️ OBS STUDIO SETUP FUNCTION
# ==========================================
def setup_obs_config():
    print(f"[*] OBS Configuration set kar raha hoon... (Stream ID: {STREAM_ID})")
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

    # 3. service.json (OK.RU RTMP URL + Selected Stream Key)
    service_json = { 
        "settings": { 
            "server": "rtmp://vsu.okcdn.ru/input/", 
            "key": ACTIVE_STREAM_KEY 
        }, 
        "type": "rtmp_custom" 
    }
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
    
    # White warning patti ko chhupane ke liye
    co.set_argument('--test-type')
    co.set_argument('--disable-infobars')
    
    # 3. Asli Chrome launch karein 
    page = ChromiumPage(addr_or_opts=co)

    # ==========================================================
    # 👇 YAHAN PAR HEADERS ADD KARNE HAIN (Link open karne se pehle) 👇
    # ==========================================================
    page.set.headers({
        'Referer': 'https://8f658612616b34dcf384fec6275a819d.dynaccent.net/',
        'Origin': 'https://8f658612616b34dcf384fec6275a819d.dynaccent.net',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)',
        'Accept-Language': 'en-US,en;q=0.9'
    })
    # ==========================================================

    # 4. Ab Headers set hone ke baad Link open karein
    page.get(TARGET_URL)

    print("[*] Website load ho chuki hai. Streaming jari hai...")
    print("[!] Testing mode: Script ab infinite loop mein chalta rahega. Rokne ke liye Action cancel karein.")

    # 5. Infinite Loop (Stream chalti rahegi)
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
