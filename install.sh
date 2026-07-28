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

echo "[*] Upgrading pip..."
pip install --upgrade pip

echo "[*] Installing Python dependencies..."
pip install python-telegram-bot==20.7
pip install requests==2.31.0
pip install urllib3==2.0.7

echo "[*] Creating directory..."
mkdir -p ~/jumman_scanner
cd ~/jumman_scanner

echo "[*] Creating jumman_scanner.py..."
cat > jumman_scanner.py << 'EOF'
# [PASTE THE FULL CODE ABOVE HERE]
EOF

echo "[*] Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
cd ~/jumman_scanner
python jumman_scanner.py
EOF

chmod +x run.sh

echo "[*] Creating shortcut..."
cat > ~/jumman << 'EOF'
#!/bin/bash
cd ~/jumman_scanner
python jumman_scanner.py
EOF

chmod +x ~/jumman
echo 'alias jumman="~/jumman"' >> ~/.bashrc

clear
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║     ✅ INSTALLATION COMPLETE!                              ║"
echo "║                                                              ║"
echo "║     🔥 Jumman Scanner installed successfully!              ║"
echo "║     👑 Owner: Jumman                                       ║"
echo "║     🔐 Password: ch71                                     ║"
echo "║                                                              ║
echo "║     📱 Bot: @JummanScannerBot                               ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📌 HOW TO RUN:"
echo ""
echo "   python ~/jumman_scanner/jumman_scanner.py"
echo "   cd ~/jumman_scanner && python jumman_scanner.py"
echo "   jumman"
echo "   ./run.sh"
echo ""
echo "🔑 PASSWORD: ch71"
echo "📱 Bot: @JummanScannerBot"
echo ""