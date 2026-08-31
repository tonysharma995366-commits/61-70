#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Miner Automation - 10 Tabs Only
"""

import os
import sys
import subprocess
import time
import psutil
from datetime import datetime
import requests
from PIL import ImageGrab
import threading

# ==================== TELEGRAM ====================
TELEGRAM_BOT_TOKEN = "8972471605:AAE7hhT8QO5N_hnfHTIX1PxRzmkRBm5voyY"
TELEGRAM_CHAT_ID = "6955911349"

class TelegramLogger:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
    
    def send_message(self, message: str):
        try:
            requests.post(f"{self.base_url}/sendMessage", 
                         json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}, 
                         timeout=10)
            print(f"✅ Telegram sent: {message[:50]}...")
        except Exception as e:
            print(f"❌ Telegram error: {e}")
    
    def send_photo(self, image_path: str, caption: str):
        try:
            with open(image_path, 'rb') as f:
                requests.post(f"{self.base_url}/sendPhoto", 
                            files={'photo': f}, 
                            data={'chat_id': TELEGRAM_CHAT_ID, 'caption': caption, 'parse_mode': 'HTML'}, 
                            timeout=30)
            os.remove(image_path)
            print(f"✅ Photo sent: {caption[:50]}...")
        except Exception as e:
            print(f"❌ Photo error: {e}")

telegram = TelegramLogger()

# ==================== CONFIG ====================
FIREFOX_PATH = "/usr/bin/firefox"
API_BASE = "https://api.unmineable.com/v5"
WALLET_ADDRESS = "nano_1g97x3h6wxd4h577p6dricapigs78ccc7tcowjfm67hewsmg7qob4xwc8jak"
COIN = "NANO"
CHECK_INTERVAL = 300  # 5 minutes

# ==================== ONLY 10 TERMINALS ====================
TERMINALS = [
    [361, "Terminal 361", "ugviq3vaogk5cjrjh2njvu", "https://ais-pre-ugviq3vaogk5cjrjh2njvu-835267516178.asia-southeast1.run.app"],
    [362, "Terminal 362", "pan3eygcye354fuowtcm4p", "https://ais-pre-pan3eygcye354fuowtcm4p-835267516178.asia-southeast1.run.app"],
    [363, "Terminal 363", "u5zgzitckdtc2dqwrcxqmg", "https://ais-pre-u5zgzitckdtc2dqwrcxqmg-835267516178.asia-southeast1.run.app"],
    [364, "Terminal 364", "lh43kfxsmzzc6ex3mmg4z5", "https://ais-pre-lh43kfxsmzzc6ex3mmg4z5-835267516178.asia-southeast1.run.app"],
    [365, "Terminal 365", "64yapvcxgoucball7ydlnq", "https://ais-pre-64yapvcxgoucball7ydlnq-835267516178.asia-southeast1.run.app"],
    [366, "Terminal 366", "nuhedif7gbpvzib7tqukfm", "https://ais-pre-nuhedif7gbpvzib7tqukfm-835267516178.asia-southeast1.run.app"],
    [367, "Terminal 367", "2u6kupvewers3l4jrw6o5b", "https://ais-pre-2u6kupvewers3l4jrw6o5b-835267516178.asia-southeast1.run.app"],
    [368, "Terminal 368", "5xb5sznynsuhqmy4xux7fz", "https://ais-pre-5xb5sznynsuhqmy4xux7fz-835267516178.asia-southeast1.run.app"],
    [369, "Terminal 369", "dz5nfkzu2becu3wzsyp7fg", "https://ais-pre-dz5nfkzu2becu3wzsyp7fg-835267516178.asia-southeast1.run.app"],
    [370, "Terminal 370", "a6caldqf6fibtgkbwlzz4b", "https://ais-pre-a6caldqf6fibtgkbwlzz4b-835267516178.asia-southeast1.run.app"],
]

# ==================== FUNCTIONS ====================
def log(msg): 
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def send_tg(title, msg, emoji="📘"):
    telegram.send_message(f"{emoji} <b>{title}</b>\n{msg}")

def get_system_info():
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        return f"CPU: {cpu}% | RAM: {ram.used/(1024**3):.1f}/{ram.total/(1024**3):.1f}GB ({ram.percent}%)"
    except:
        return "N/A"

def take_screenshot(filename="screenshot.png"):
    try:
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        return filename
    except Exception as e:
        log(f"Screenshot error: {e}")
        return None

def get_uuid():
    try:
        r = requests.get(f"{API_BASE}/address/{WALLET_ADDRESS}?coin={COIN}", 
                        headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        data = r.json()
        uuid = data.get('data', {}).get('uuid')
        log(f"✅ Got UUID: {uuid}")
        return uuid
    except Exception as e:
        log(f"❌ UUID error: {e}")
        return None

def check_status(miner_name, uuid):
    try:
        r = requests.get(f"{API_BASE}/account/{uuid}/workers", 
                        headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        workers = r.json().get('data', {}).get('randomx', {}).get('workers', [])
        for w in workers:
            if w.get('name') == miner_name:
                return w.get('online', False)
        return False
    except Exception as e:
        log(f"Status check error: {e}")
        return False

def open_firefox_window(url, name):
    try:
        subprocess.Popen([FIREFOX_PATH, "--new-window", url, "--kiosk"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL,
                        env={'DISPLAY': ':1'})
        log(f"✅ Opened: {name}")
        return True
    except Exception as e:
        log(f"❌ Error opening {name}: {e}")
        return False

def close_firefox_windows():
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'firefox' or proc.info['name'] == 'firefox-bin':
                proc.terminate()
        time.sleep(2)
        log("✅ Closed all Firefox windows")
        return True
    except Exception as e:
        log(f"❌ Close error: {e}")
        return False

def send_startup_notification():
    try:
        # Send initial message with system info
        msg = f"""🚀 <b>SYSTEM STARTED</b>
        
📍 Total Miners: {len(TERMINALS)}
🖥️ {get_system_info()}
⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>Active Terminals:</b>
"""
        for term in TERMINALS:
            msg += f"• {term[1]} - {term[3]}\n"
        
        telegram.send_message(msg)
    except Exception as e:
        log(f"Startup notification error: {e}")

# ==================== MAIN ====================
def main():
    log("🚀 Starting miner automation with 10 tabs...")
    
    # Send startup notification
    send_startup_notification()
    
    # Get UUID
    uuid = get_uuid()
    if not uuid:
        send_tg("❌ ERROR", "Failed to get UUID!\nCheck wallet address and coin.", "❌")
        log("❌ Failed to get UUID, exiting...")
        return
    
    send_tg("✅ UUID FOUND", f"UUID: {uuid}", "✅")
    
    # Open all terminals
    log("📂 Opening terminals...")
    for idx, term in enumerate(TERMINALS, 1):
        log(f"Opening {idx}/{len(TERMINALS)}: {term[1]}")
        open_firefox_window(term[3], term[1])
        time.sleep(3)  # 3 second gap between each
    
    log("✅ All terminals opened!")
    send_tg("✅ ALL OPENED", 
            f"All {len(TERMINALS)} terminals opened successfully!\n{get_system_info()}", 
            "✅")
    
    # Take initial screenshot
    time.sleep(10)
    ss = take_screenshot("initial_screenshot.png")
    if ss:
        telegram.send_photo(ss, f"📸 <b>Initial Screenshot</b>\n{get_system_info()}")
    
    # Monitoring loop
    iteration = 0
    while True:
        time.sleep(CHECK_INTERVAL)
        iteration += 1
        
        log(f"🔍 Checking status (Iteration {iteration})...")
        
        offline = []
        online = 0
        
        for term in TERMINALS:
            status = check_status(term[2], uuid)
            if status:
                online += 1
            else:
                offline.append(term)
        
        log(f"📊 Status: {online}/{len(TERMINALS)} online, {len(offline)} offline")
        
        if offline:
            offline_names = ", ".join([f"{t[1]}" for t in offline[:5]])
            if len(offline) > 5:
                offline_names += f" and {len(offline)-5} more..."
            
            send_tg(f"⚠️ {len(offline)} OFFLINE", 
                    f"Online: {online}/{len(TERMINALS)}\nOffline: {offline_names}\n{get_system_info()}\n\n🔄 Restarting offline miners...", 
                    "⚠️")
            
            # Close all and reopen offline ones
            close_firefox_windows()
            time.sleep(5)
            
            # Reopen only offline terminals
            log(f"🔄 Reopening {len(offline)} offline terminals...")
            for term in offline:
                open_firefox_window(term[3], term[1])
                time.sleep(3)
            
            log("✅ Restart complete!")
            send_tg("🔄 RESTART COMPLETE", 
                    f"Restarted {len(offline)} miners\n{get_system_info()}", 
                    "✅")
            
            # Take screenshot after restart
            time.sleep(10)
            ss = take_screenshot(f"screenshot_iter_{iteration}.png")
            if ss:
                telegram.send_photo(ss, f"📸 <b>After Restart</b>\nIteration: {iteration}\n{get_system_info()}")
        else:
            log("✅ All miners are online!")
            send_tg("✅ ALL ONLINE", 
                    f"{online}/{len(TERMINALS)} ONLINE (100%)\n{get_system_info()}\nIteration: {iteration}", 
                    "✅")

if __name__ == "__main__":
    # Set display
    os.environ['DISPLAY'] = ':1'
    
    try:
        main()
    except KeyboardInterrupt:
        log("🛑 Stopped by user")
        send_tg("🛑 STOPPED", "System stopped by user", "🛑")
    except Exception as e:
        log(f"💀 Fatal error: {e}")
        send_tg("💀 FATAL ERROR", f"Error: {str(e)}\nCheck logs for details.", "💀")
        raise
