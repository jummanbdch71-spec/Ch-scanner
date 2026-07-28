#!/bin/bash

clear

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║
echo "║     🌐 ROUTER HACKER - VULNERABILITY CHECKER 🌐           ║
echo "║     🔍 Check Vulnerability First, Then Crack              ║
echo "║     ⚡ Skip Secure Routers - Only Hack Vulnerable Ones    ║
echo "║     👑 Owner: Jumman                                       ║
echo "║     🔐 Password: ch71                                     ║
echo "║                                                              ║
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

if [ ! -d "$PREFIX" ]; then
    echo "❌ This script is for Termux only!"
    exit 1
fi

echo "[*] Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo "[*] Installing required packages..."
pkg install -y python python-pip git wget curl nmap

echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install requests

echo "[*] Creating directory..."
mkdir -p ~/router_hacker
cd ~/router_hacker

echo "[*] Creating router_hacker.py..."
curl -sSL -o router_hacker.py "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/router_hacker.py"

echo "[*] Creating run script..."
cat > run.sh << 'RUNEOF'
#!/bin/bash
cd ~/router_hacker
python router_hacker.py
RUNEOF

chmod +x run.sh

echo "[*] Creating shortcut..."
cat > ~/routerhack << 'SHORTCUTEOF'
#!/bin/bash
cd ~/router_hacker
python router_hacker.py
SHORTCUTEOF

chmod +x ~/routerhack
echo 'alias routerhack="~/routerhack"' >> ~/.bashrc
source ~/.bashrc

clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║
echo "║     ✅ INSTALLATION COMPLETE!                              ║
echo "║                                                              ║
echo "║     🌐 Router Hacker - Vulnerability Checker installed!    ║
echo "║     👑 Owner: Jumman                                       ║
echo "║     🔐 Password: ch71                                     ║
echo "║     ⚡ Check Vulnerability First, Then Crack              ║
echo "║     💀 Skip Secure Routers - Only Hack Vulnerable Ones    ║
echo "║                                                              ║
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📌 HOW TO RUN:"
echo "   1️⃣  routerhack"
echo "   2️⃣  cd ~/router_hacker && python router_hacker.py"
echo ""
echo "🔑 PASSWORD: ch71"
echo ""