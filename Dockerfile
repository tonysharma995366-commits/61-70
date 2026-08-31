FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Base packages
RUN apt update -y && apt install --no-install-recommends -y \
    xfce4 xfce4-goodies tigervnc-standalone-server novnc websockify \
    sudo xterm init systemd snapd vim net-tools curl wget git tzdata \
    dbus-x11 x11-utils x11-xserver-utils x11-apps software-properties-common \
    python3 python3-pip firefox xubuntu-icon-theme

# Firefox preferences
RUN add-apt-repository ppa:mozillateam/ppa -y && \
    echo 'Package: *' >> /etc/apt/preferences.d/mozilla-firefox && \
    echo 'Pin: release o=LP-PPA-mozillateam' >> /etc/apt/preferences.d/mozilla-firefox && \
    echo 'Pin-Priority: 1001' >> /etc/apt/preferences.d/mozilla-firefox && \
    echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:jammy";' | tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox

# Python dependencies
RUN pip3 install requests psutil pillow

# Create Xauthority
RUN touch /root/.Xauthority

# Copy scripts
COPY miner_script.py /root/miner_script.py
COPY start.sh /root/start.sh
RUN chmod +x /root/miner_script.py /root/start.sh

EXPOSE 5901
EXPOSE 6080

CMD ["/root/start.sh"]
