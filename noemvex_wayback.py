#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NOEMVEX-WAYBACK v1.0 [CHRONOS EDITION]
Author: Emre 'noemvex' Sahin
Description: Advanced Historical OSINT Engine. Scrapes and filters Wayback Machine snapshots
             to discover sensitive artifacts, hardcoded keys, and forgotten endpoints.
"""

import os
import sys
import requests
import argparse
import re
import time
from datetime import datetime

# --- STANDARD UI CLASS (Unified Noemvex Design System) ---
class UI:
    PURPLE = '\033[95m'  
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    GREY = '\033[90m'
    END = '\033[0m'

    @staticmethod
    def banner():
        # Raw string (r"") 
        ascii_art = [
            r"███╗   ██╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗███████╗██╗  ██╗",
            r"████╗  ██║██╔═══██╗██╔════╝████╗ ████║██║   ██║██╔════╝╚██╗██╔╝",
            r"██╔██╗ ██║██║   ██║█████╗  ██╔████╔██║██║   ██║█████╗   ╚███╔╝ ",
            r"██║╚██╗██║██║   ██║██╔══╝  ██║╚██╔╝██║╚██╗ ██╔╝██╔══╝   ██╔██╗ ",
            r"██║ ╚████║╚██████╔╝███████╗██║ ╚═╝ ██║ ╚████╔╝ ███████╗██╗  ██╗",
            r"╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝"
        ]
        
        print(f"{UI.GREEN}{UI.BOLD}")
        for line in ascii_art:
            print(line)
        print(f"               {UI.PURPLE}[ WAYBACK CHRONOS EDITION v1.0 ]{UI.END}\n")

# --- CORE ENGINE ---
class ChronosEngine:
    def __init__(self, domain, output_file=None):
        self.domain = domain
        self.output_file = output_file
        # Senior Fix: Robust URL normalization
        self.clean_domain = domain.replace("https://", "").replace("http://", "").split("/")[0]
        
        # CDX API: Optimized for speed (fl=original, collapse=urlkey)
        self.api_url = f"http://web.archive.org/cdx/search/cdx?url=*.{self.clean_domain}/*&output=json&fl=original&collapse=urlkey"
        self.findings = []

        # MASTER UPDATE: Regex now handles query parameters (e.g., config.php?v=1)
        # Using (?:$|\?) to match end of string OR start of query string
        self.patterns = {
            "Configuration": re.compile(r"\.(env|yml|yaml|config|ini|conf|xml|json|dockerfile|bak|swp)(?:$|\?)", re.IGNORECASE),
            "Database": re.compile(r"\.(sql|db|sqlite|mdb|dump|backup|log)(?:$|\?)", re.IGNORECASE),
            "Source Code": re.compile(r"\.(git|svn|sh|py|php|pl|rb|go|asp|aspx|jsp)(?:$|\?)", re.IGNORECASE),
            "Documents": re.compile(r"\.(doc|docx|xls|xlsx|pdf|txt|csv)(?:$|\?)", re.IGNORECASE),
            "Keys/Secrets": re.compile(r"(api_key|secret|token|auth|password|jenkins|id_rsa|aws_access_key_id)", re.IGNORECASE)
        }
        
        # Noise Filter: Ignore static assets even if they have query params
        self.noise = re.compile(r"\.(jpg|jpeg|png|gif|css|svg|woff|ttf|ico|mp4|mp3)(?:$|\?)", re.IGNORECASE)

    def check_root(self):
        """Security Protocol: Root Privilege Check (Cross-Platform Safe)"""
        # Senior Fix: safely check for root on Unix, skip on Windows to prevent crash
        if hasattr(os, 'geteuid'):
            if os.geteuid() != 0:
                UI.log("Running without ROOT privileges. Socket stability might be affected.", "WARN")
        else:
            # On Windows or non-Posix, we just skip the check silently or warn
            pass

    def fetch_data(self):
        """Phase 1: Retrieving Historical Snapshots"""
        UI.log(f"Initiating Time-Travel connection to Archive.org for: {UI.BOLD}{self.clean_domain}{UI.END}")
        try:
            # Senior Fix: 45s timeout to handle massive datasets
            response = requests.get(self.api_url, timeout=45)
            
            if response.status_code == 200:
                data = response.json()
                if len(data) > 0:
                    data.pop(0) # Remove header row
                
                count = len(data)
                UI.log(f"Data retrieved successfully. Total unique snapshots: {UI.BOLD}{count}{UI.END}", "SUCCESS")
                return [item[0] for item in data]
            elif response.status_code == 404:
                UI.log("No archived data found for this target.", "WARN")
                return []
            else:
                UI.log(f"Archive API returned unexpected status: {response.status_code}", "CRITICAL")
                return []
        except requests.exceptions.Timeout:
            UI.log("Connection timed out. The Archive API is currently overloaded.", "CRITICAL")
            return []
        except Exception as e:
            UI.log(f"Fatal Error during fetch: {e}", "CRITICAL")
            return []

    def analyze(self, urls):
        """Phase 2: Intelligent Pattern Matching Engine"""
        UI.log("Starting NOEMVEX Heuristic Analysis Engine...", "INFO")
        
        start_time = time.time()
        found_count = 0

        for url in urls:
            if self.noise.search(url):
                continue
            
            for category, regex in self.patterns.items():
                if regex.search(url):
                    self.findings.append({"category": category, "url": url})
                    found_count += 1
                    
                    # Visual Feedback for Critical Findings
                    if category in ["Configuration", "Database", "Keys/Secrets"]:
                        print(f"    {UI.RED}>> [CRITICAL] {category.upper()}: {url}{UI.END}")
                    elif category == "Source Code":
                         print(f"    {UI.YELLOW}>> [SENSITIVE] {category.upper()}: {url}{UI.END}")
                    break 
        
        duration = time.time() - start_time
        UI.log(f"Analysis completed in {duration:.2f} seconds. Artifacts found: {found_count}", "SUCCESS")

    def save_report(self):
        """Phase 3: Intelligence Reporting"""
        if not self.findings:
            return

        filename = self.output_file if self.output_file else f"chronos_report_{self.clean_domain}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("NOEMVEX-WAYBACK [CHRONOS EDITION] - INTELLIGENCE REPORT\n")
                f.write(f"Target: {self.clean_domain}\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*60 + "\n\n")
                
                # Grouping for professional readability
                categories = {}
                for item in self.findings:
                    cat = item['category']
                    if cat not in categories:
                        categories[cat] = []
                    categories[cat].append(item['url'])
                
                for cat, urls in categories.items():
                    f.write(f"[+] {cat.upper()} ({len(urls)} items)\n")
                    for u in urls:
                        f.write(f"    {u}\n")
                    f.write("\n")
            
            UI.log(f"Full report exported to: {UI.BOLD}{filename}{UI.END}", "SUCCESS")
        except Exception as e:
            UI.log(f"Report generation failed: {e}", "CRITICAL")

    def run(self):
        UI.banner()
        self.check_root()
        
        urls = self.fetch_data()
        if urls:
            self.analyze(urls)
            self.save_report()
        
        print(f"\n{UI.BOLD}{UI.GREEN}[√] OPERATION CHRONOS COMPLETED.{UI.END}")

if __name__ == "__main__":

    UI.banner() 

    parser = argparse.ArgumentParser(description="NOEMVEX-WAYBACK: Chronos Edition")
    parser.add_argument('-d', '--domain', required=True, help='Target domain (e.g., tesla.com)')
    parser.add_argument('-o', '--output', help='Custom output filename')
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    
    engine = ChronosEngine(args.domain, args.output)
    engine.run()