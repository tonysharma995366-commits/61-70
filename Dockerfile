FROM --platform=linux/amd64 ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install GUI + RDP + SSH + Tools
RUN apt update -y && apt install --no-install-recommends -y \
    xfce4 xfce4-goodies \
    tigervnc-standalone-server \
    novnc websockify \
    sudo xterm \
    net-tools curl wget git vim \
    python3 python3-pip \
    dbus-x11 x11-utils \
    x11-xserver-utils \
    openssh-server \
    openssh-client \
    sshpass \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install requests psutil

# Setup SSH
RUN mkdir -p /var/run/sshd && \
    echo 'root:admin123' | chpasswd && \
    useradd -m -s /bin/bash ubuntu && \
    echo 'ubuntu:admin123' | chpasswd && \
    usermod -aG sudo ubuntu && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/#AllowTcpForwarding yes/AllowTcpForwarding yes/' /etc/ssh/sshd_config

# Copy scripts
COPY script.py /root/script.py
COPY start.sh /root/start.sh
RUN chmod +x /root/script.py /root/start.sh

EXPOSE 22 5901 6080

CMD ["/root/start.sh"]
