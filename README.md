# Ubuntu RDP with Miner Automation

## Description
This Docker container provides:
- Ubuntu 22.04 with XFCE desktop
- VNC server access via web browser (port 6080)
- Automatic miner script with 10 tabs only
- Telegram notifications

## Deployment on Railway

### Steps:
1. Create a GitHub repository
2. Add these files to the repository
3. Go to Railway.app
4. Connect your GitHub repository
5. Deploy

## Access
- Web VNC: `https://your-railway-app.railway.app`
- Port: 6080

## Features
- Automatic startup of miner script
- Telegram notifications with new bot token
- Screenshot capture and sending
- Auto-restart of offline miners
- 10 tabs only (reduced from 90)

## Telegram Bot
Token: 8972471605:AAE7hhT8QO5N_hnfHTIX1PxRzmkRBm5voyY
Chat ID: 6955911349

## Environment Variables (Optional)
No environment variables required - all configured in script.
