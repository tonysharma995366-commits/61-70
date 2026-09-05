#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ubuntu GUI + SSH + Telegram Bot with SSH Commands
"""

import os
import sys
import time
import subprocess
import requests
import psutil
from datetime import datetime
import socket
import threading
import json

# ==================== TELEGRAM CONFIG ====================
TELEGRAM_BOT_TOKEN = "8972471605:AAE7hhT8QO5N_hnfHTIX1PxRzmkRBm5voyY"
TELEGRAM_CHAT_ID = "6955911349"

# ==================== TELEGRAM BOT CLASS ====================
class TelegramBot:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
        self.last_update_id = 0
        self.bot_username = None
        self.get_bot_info()
    
    def get_bot_info(self):
        """Get bot username"""
        try:
            response = requests.get(f"{self.base_url}/getMe", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['ok']:
                    self.bot_username = data['result']['username']
                    print(f"✅ Bot username: @{self.bot_username}")
        except:
            pass
    
    def send_message(self, message):
        """Send message to Telegram"""
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML",
                "disable_web_page_preview": True
            }
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                print(f"✅ Message sent")
                return True
            else:
                print(f"❌ Failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Telegram error: {e}")
            return False
    
    def get_updates(self):
        """Get new messages from Telegram"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {
                'offset': self.last_update_id + 1,
                'timeout': 30,
                'limit': 10
            }
            response = requests.get(url, params=params, timeout=35)
            if response.status_code == 200:
                data = response.json()
                if data['ok'] and data['result']:
                    for update in data['result']:
                        self.last_update_id = update['update_id']
                        if 'message' in update:
                            return update['message']
            return None
        except Exception as e:
            print(f"❌ Get updates error: {e}")
            return None

bot = TelegramBot()

# ==================== SYSTEM FUNCTIONS ====================

def get_public_ip():
    """Get public IP"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        try:
            response = requests.get('https://ifconfig.me', timeout=5)
            return response.text.strip()
        except:
            return "Unknown"

def get_ssh_command():
    """Generate SSH command"""
    try:
        public_ip = get_public_ip()
        
        ssh_cmd = f"""
🔑 <b>SSH CONNECTION COMMAND</b>
━━━━━━━━━━━━━━━━━━━━━

<b>📱 Termux SSH Command:</b>
<code>ssh root@{public_ip} -p 22</code>

<b>🔐 With Password:</b>
<code>sshpass -p 'admin123' ssh root@{public_ip} -p 22</code>

<b>👤 Ubuntu User:</b>
<code>ssh ubuntu@{public_ip} -p 22</code>

<b>📋 Login Details:</b>
👤 Username: <code>root</code> or <code>ubuntu</code>
🔐 Password: <code>admin123</code>
🌐 Host: <code>{public_ip}</code>
📡 Port: <code>22</code>

━━━━━━━━━━━━━━━━━━━━━

<b>📱 Termux Setup:</b>
<code>pkg update && pkg upgrade
pkg install openssh sshpass
ssh root@{public_ip}</code>

<b>✅ After SSH Connect:</b>
<code>cd /root
ls -la
python3 script.py</code>
"""
        return ssh_cmd
    except Exception as e:
        return f"❌ Error: {e}"

def get_system_status():
    """Get system status"""
    try:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Check services
        ssh_status = "✅ Running" if check_service('ssh') else "❌ Stopped"
        vnc_status = "✅ Running" if check_service('vnc') else "❌ Stopped"
        web_status = "✅ Running" if check_service('websockify') else "❌ Stopped"
        
        status = f"""
🖥️ <b>SYSTEM STATUS</b>
━━━━━━━━━━━━━━━━━━━━━
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

<b>📊 Resources:</b>
🔄 CPU: {cpu}%
💾 RAM: {ram.used/(1024**3):.1f}/{ram.total/(1024**3):.1f}GB ({ram.percent}%)
💿 Disk: {disk.used/(1024**3):.1f}/{disk.total/(1024**3):.1f}GB ({disk.percent}%)

<b>🔧 Services:</b>
🔐 SSH: {ssh_status}
🖥️ VNC: {vnc_status}
🌐 WebVNC: {web_status}

<b>🌐 Network:</b>
🌍 Public IP: {get_public_ip()}
🏠 Hostname: {socket.gethostname()}

━━━━━━━━━━━━━━━━━━━━━
✅ System operational!
"""
        return status
    except Exception as e:
        return f"❌ Error: {e}"

def check_service(service_name):
    """Check if service is running"""
    try:
        if service_name == 'vnc':
            result = subprocess.run("ps aux | grep -E 'vnc|tigervnc' | grep -v grep", shell=True, capture_output=True)
            return result.returncode == 0 and result.stdout
        elif service_name == 'websockify':
            result = subprocess.run("ps aux | grep websockify | grep -v grep", shell=True, capture_output=True)
            return result.returncode == 0 and result.stdout
        else:
            result = subprocess.run(f"service {service_name} status", shell=True, capture_output=True)
            return result.returncode == 0 and "running" in result.stdout.decode()
    except:
        return False

def run_command(cmd):
    """Run shell command"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'code': result.returncode
        }
    except Exception as e:
        return {'success': False, 'output': '', 'error': str(e), 'code': -1}

def get_active_sessions():
    """Get active SSH sessions"""
    try:
        result = run_command("who")
        if result['success'] and result['output']:
            sessions = result['output'].strip()
            return f"👥 <b>Active Sessions:</b>\n<code>{sessions}</code>"
        return "👥 No active SSH sessions"
    except:
        return "👥 Unable to check sessions"

# ==================== TELEGRAM COMMAND HANDLER ====================

def handle_telegram_commands():
    """Handle incoming Telegram messages"""
    print("🤖 Telegram command handler started...")
    
    while True:
        try:
            message = bot.get_updates()
            if message:
                # Check if message is from our chat
                if 'chat' in message and str(message['chat']['id']) == TELEGRAM_CHAT_ID:
                    text = message.get('text', '').lower()
                    username = message.get('from', {}).get('first_name', 'User')
                    
                    print(f"📩 Message from {username}: {text}")
                    
                    # Handle commands
                    if text == '/start' or text == '/help':
                        response = f"""
🚀 <b>WELCOME TO UBUNTU GUI SSH BOT</b>
━━━━━━━━━━━━━━━━━━━━━

<b>📋 Available Commands:</b>
/ssh - Get SSH command
/status - System status
/sessions - Active SSH sessions
/restart - Restart SSH
/ip - Get public IP
/help - Show this help

<b>🔑 Quick Connect:</b>
<code>ssh root@{get_public_ip()} -p 22</code>
Password: admin123
"""
                        bot.send_message(response)
                    
                    elif text == '/ssh':
                        bot.send_message(get_ssh_command())
                    
                    elif text == '/status':
                        bot.send_message(get_system_status())
                    
                    elif text == '/sessions':
                        sessions = get_active_sessions()
                        bot.send_message(f"👥 <b>ACTIVE SSH SESSIONS</b>\n━━━━━━━━━━━━━━━━━━━━━\n{sessions}")
                    
                    elif text == '/restart':
                        bot.send_message("🔄 <b>RESTARTING SSH SERVICE</b>...")
                        result = run_command("service ssh restart")
                        if result['success']:
                            bot.send_message(f"✅ <b>SSH RESTARTED SUCCESSFULLY</b>\n\n{get_ssh_command()}")
                        else:
                            bot.send_message(f"❌ <b>SSH RESTART FAILED</b>\nError: {result['error']}")
                    
                    elif text == '/ip':
                        ip = get_public_ip()
                        bot.send_message(f"🌐 <b>PUBLIC IP</b>\n━━━━━━━━━━━━━━━━━━━━━\n<code>{ip}</code>\n\n🔑 SSH: <code>ssh root@{ip} -p 22</code>")
                    
                    elif 'ssh' in text or 'connect' in text:
                        bot.send_message(get_ssh_command())
                    
                    else:
                        response = f"""
❓ <b>Unknown Command</b>

Type <code>/help</code> to see all commands.

<b>Quick Connect:</b>
{get_ssh_command()}
"""
                        bot.send_message(response)
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Command handler error: {e}")
            time.sleep(5)

# ==================== MAIN ====================

def main():
    # Send startup message
    startup_msg = f"""
🚀 <b>UBUNTU GUI + SSH STARTED</b>
━━━━━━━━━━━━━━━━━━━━━
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{get_system_status()}

━━━━━━━━━━━━━━━━━━━━━
<b>🔑 SSH Command:</b>
<code>ssh root@{get_public_ip()} -p 22</code>
Password: admin123

<b>🤖 Bot Commands:</b>
/ssh - Get SSH command
/status - System status
/sessions - Active sessions
/restart - Restart SSH
/ip - Get public IP
/help - Help menu
━━━━━━━━━━━━━━━━━━━━━
"""
    bot.send_message(startup_msg)
    
    # Start Telegram command handler in background
    print("🤖 Starting Telegram command handler...")
    command_thread = threading.Thread(target=handle_telegram_commands, daemon=True)
    command_thread.start()
    
    # ============================================
    # YOUR CUSTOM SCRIPT LOGIC HERE
    # ============================================
    
    # Create info file
    with open('/root/SSH_INFO.txt', 'w') as f:
        f.write(f"""
========================================
  🚀 SSH CONNECTION INFO
========================================
Public IP: {get_public_ip()}
SSH Port: 22
Username: root
Password: admin123

Command: ssh root@{get_public_ip()} -p 22
========================================
""")
    
    # Create test script
    test_script = """#!/usr/bin/env python3
import time
import socket

print("=== SSH Test Script ===")
print(f"Hostname: {socket.gethostname()}")
print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=== Script Complete ===")
"""
    with open('/root/test.py', 'w') as f:
        f.write(test_script)
    
    # ============================================
    # MONITORING LOOP
    # ============================================
    
    iteration = 0
    while True:
        try:
            iteration += 1
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log to file
            with open('/root/script_log.txt', 'a') as f:
                f.write(f"[{current_time}] Iteration {iteration} | SSH: {check_service('ssh')}\n")
            
            # Send SSH info every 6 hours
            if iteration % 72 == 0:  # 72 * 300 sec = 6 hours
                ssh_info = f"""
🔄 <b>SSH CONNECTION REMINDER</b>
━━━━━━━━━━━━━━━━━━━━━
⏰ Time: {current_time}

{get_ssh_command()}

<b>Active Sessions:</b>
{get_active_sessions()}
"""
                bot.send_message(ssh_info)
            
            # Send status every 2 hours
            if iteration % 24 == 0:  # 24 * 300 sec = 2 hours
                bot.send_message(get_system_status())
            
            # Check SSH service
            if iteration % 6 == 0:  # Every 30 minutes
                if not check_service('ssh'):
                    bot.send_message("⚠️ <b>SSH SERVICE DOWN</b>\nRestarting...")
                    run_command("service ssh restart")
                    time.sleep(5)
                    if check_service('ssh'):
                        bot.send_message("✅ <b>SSH RESTARTED</b>")
            
            time.sleep(300)  # 5 minutes
            
        except Exception as e:
            error_msg = f"""
❌ <b>ERROR IN MAIN LOOP</b>
━━━━━━━━━━━━━━━━━━━━━
⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Error: {str(e)}
"""
            bot.send_message(error_msg)
            time.sleep(60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        bot.send_message("🛑 <b>SCRIPT STOPPED</b>\nStopped by user")
    except Exception as e:
        bot.send_message(f"💀 <b>FATAL ERROR</b>\n{str(e)}")
        sys.exit(1)
