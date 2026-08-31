#!/bin/bash

echo "Starting VNC server..."
vncserver -localhost no -SecurityTypes None -geometry 1024x768 --I-KNOW-THIS-IS-INSECURE

echo "Starting websockify..."
openssl req -new -subj "/C=JP" -x509 -days 365 -nodes -out /root/self.pem -keyout /root/self.pem
websockify -D --web=/usr/share/novnc/ --cert=/root/self.pem 6080 localhost:5901

# Wait for VNC to be ready
echo "Waiting for VNC to initialize..."
sleep 10

# Set DISPLAY
export DISPLAY=:1

echo "Starting Python miner script..."
cd /root
python3 /root/miner_script.py

# Keep container running
tail -f /dev/null
