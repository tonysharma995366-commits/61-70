#!/bin/bash

echo "========================================="
echo "  🚀 Ubuntu GUI + SSH + Telegram Bot"
echo "========================================="

# Start SSH server
echo "Starting SSH server..."
service ssh start

# Create SSH directory
mkdir -p /root/.ssh
chmod 700 /root/.ssh

# Start VNC server
echo "Starting VNC server..."
vncserver -localhost no -SecurityTypes None -geometry 1280x720 --I-KNOW-THIS-IS-INSECURE

# Start WebVNC
echo "Starting WebVNC..."
openssl req -new -subj "/C=JP" -x509 -days 365 -nodes -out /root/self.pem -keyout /root/self.pem
websockify -D --web=/usr/share/novnc/ --cert=/root/self.pem 6080 localhost:5901

# Wait for GUI
sleep 5

# Set display
export DISPLAY=:1

# Open terminal in GUI
echo "Opening terminal in GUI..."
DISPLAY=:1 xfce4-terminal --geometry=90x30 --title="Ubuntu Terminal (SSH Enabled)" &

# Run Python script
echo "Starting Python script with Telegram bot..."
cd /root
python3 /root/script.py &

echo "========================================="
echo "  ✅ ALL SERVICES STARTED!"
echo "========================================="
echo "  📱 WebVNC: http://localhost:6080"
echo "  🔑 SSH: ssh root@localhost -p 22"
echo "  🔐 Password: admin123"
echo "  🤖 Telegram Bot: Active"
echo "========================================="

# Keep container alive
tail -f /dev/null
