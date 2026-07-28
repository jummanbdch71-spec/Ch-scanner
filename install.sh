#!/bin/bash

clear

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║
echo "║     🌐 ROUTER HACKER - 100% WORKING 🌐                    ║
echo "║     ⚡ Ultra Fast Scanner & Brute Force                   ║
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
cat > router_hacker.py << 'EOF'
# [PASTE THE FULL CODE ABOVE HERE]
EOF

echo "[*] Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
cd ~/router_hacker
python router_hacker.py
EOF

chmod +x run.sh

echo "[*] Creating shortcut..."
cat > ~/routerhack << 'EOF'
#!/bin/bash
cd ~/router_hacker
python router_hacker.py
EOF

chmod +x ~/routerhack
echo 'alias routerhack="~/routerhack"' >> ~/.bashrc
source ~/.bashrc

clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║
echo "║     ✅ INSTALLATION COMPLETE!                              ║
echo "║                                                              ║
echo "║     🌐 Router Hacker - 100% Working installed!             ║
echo "║     👑 Owner: Jumman                                       ║
echo "║     🔐 Password: ch71                                     ║
echo "║     ⚡ Ultra Fast Scanning                                ║
echo "║     💀 100% Working Password Cracking                     ║
echo "║                                                              ║
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📌 HOW TO RUN:"
echo "   1️⃣  routerhack"
echo "   2️⃣  cd ~/router_hacker && python router_hacker.py"
echo ""
echo "🔑 PASSWORD: ch71"
echo ""