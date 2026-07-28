#!/bin/bash

clear

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     🔥 JUMMAN SCANNER - TERMUX INSTALLER 🔥               ║"
echo "║     📷 IP Camera & Router Scanner                          ║"
echo "║     👑 Owner: Jumman                                       ║"
echo "║     🔐 Password: ch71                                     ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Termux
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
pip install python-telegram-bot==13.7 requests

echo "[*] Creating directory..."
mkdir -p ~/jumman_scanner
cd ~/jumman_scanner

echo "[*] Downloading Jumman Scanner..."
if [ -f "jumman_scanner.py" ]; then
    echo "[✓] File already exists"
else
    curl -sSL -o jumman_scanner.py "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/jumman_scanner.py"
fi

echo "[*] Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
cd ~/jumman_scanner
python jumman_scanner.py
EOF

chmod +x run.sh

echo "[*] Creating desktop shortcut..."
cat > ~/jumman << 'EOF'
#!/bin/bash
cd ~/jumman_scanner
python jumman_scanner.py
EOF

chmod +x ~/jumman
echo 'alias jumman="~/jumman"' >> ~/.bashrc
source ~/.bashrc

clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     ✅ INSTALLATION COMPLETE!                              ║"
echo "║                                                              ║"
echo "║     🔥 Jumman Scanner installed successfully!              ║"
echo "║     👑 Owner: Jumman                                       ║"
echo "║     🔐 Password: ch71                                     ║"
echo "║                                                              ║"
echo "║     📱 Bot: @JummanScannerBot                               ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📌 HOW TO RUN:"
echo ""
echo "   1️⃣  python ~/jumman_scanner/jumman_scanner.py"
echo ""
echo "   2️⃣  cd ~/jumman_scanner && python jumman_scanner.py"
echo ""
echo "   3️⃣  jumman (if you added alias)"
echo ""
echo "   4️⃣  ./run.sh"
echo ""
echo "🔑 PASSWORD: ch71"
echo "📱 Bot: @JummanScannerBot"
echo ""