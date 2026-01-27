# NOEMVEX-WAYBACK v1.0 [CHRONOS EDITION]
![Python](https://img.shields.io/badge/Python-3.x-blue) ![License](https://img.shields.io/badge/License-MIT-grey) ![Focus](https://img.shields.io/badge/Focus-Historical%20OSINT-orange) ![Edition](https://img.shields.io/badge/Edition-Chronos%20Edition-cyan)

> **"Hunt the Assets, Map the Surface."**
> Lightweight Web Reconnaissance engine designed for passive subdomain enumeration, security header analysis, and sensitive file discovery.
> ⚠️ **Disclaimer:** This tool is for educational purposes only. [Read the full Legal Disclaimer](#️-legal-disclaimer)

---

##  About
**NOEMVEX-WAYBACK** is a passive reconnaissance tool developed to perform deep historical analysis on target domains. By leveraging the massive database of the Wayback Machine (Archive.org), it travels back in time to identify forgotten backup files, old configuration scripts (.env, wp-config), and hardcoded API keys that were once public but are now deleted from the live site. It operates completely **off-grid**, meaning it never interacts directly with the target server, ensuring total stealth.

##  Capabilities
* **Zero-Touch Recon:** Performs deep analysis without sending a single packet to the target infrastructure, bypassing WAFs and IDS.
* **Intelligent Pattern Matching:** Uses pre-compiled Regex engines to filter thousands of URLs and pinpoint high-value targets (Config, Database, Secrets).
* **High-Performance Engine:** Optimized CDX API queries with `urlkey` collapsing to handle massive datasets in seconds.
* **Noise Cancellation:** Automatically filters out static assets (images, fonts, css) to focus purely on actionable intelligence.
* **Smart Reporting:** Generates categorized, clean reports ready for professional review and further exploitation.

---

##  Usage

### 1. Requirements
Standard Python 3.x is required. Ensure you have the requests library installed:

    pip install -r requirements.txt

### 2. Execution

    # Clone the Chronos Engine
    git clone https://github.com/noemvex/noemvex-wayback.git
    cd noemvex-wayback

    # Basic Usage (Display results on screen)
    python3 noemvex_wayback.py -d example.com

    # Recommended Usage (Save output to report file)
    python3 noemvex_wayback.py -d example.com -o target_intel.txt

---

##  Output Preview

    ███╗   ██╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗███████╗██╗  ██╗
    ████╗  ██║██╔═══██╗██╔════╝████╗ ████║██║   ██║██╔════╝╚██╗██╔╝
    ██╔██╗ ██║██║   ██║█████╗  ██╔████╔██║██║   ██║█████╗   ╚███╔╝ 
    ██║╚██╗██║██║   ██║██╔══╝  ██║╚██╔╝██║╚██╗ ██╔╝██╔══╝   ██╔██╗ 
    ██║ ╚████║╚██████╔╝███████╗██║ ╚═╝ ██║ ╚████╔╝ ███████╗██╗  ██╗
    ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝
                   [ WAYBACK CHRONOS EDITION v1.0 ]

    [INFO] Initiating Time-Travel connection to Archive.org for: example.com
    [SUCCESS] Data retrieved successfully. Total unique snapshots: 14,205

    [INFO] Starting NOEMVEX Heuristic Analysis Engine...
        >> [CRITICAL] DATABASE: http://web.archive.org/web/202105/example.com/backup.sql.gz
        >> [CRITICAL] CONFIGURATION: http://web.archive.org/web/202008/example.com/.env
        >> [SENSITIVE] SOURCE CODE: http://web.archive.org/web/201911/example.com/test_api.php

    [SUCCESS] Analysis completed in 1.42 seconds. Artifacts found: 3
    [SUCCESS] Full report exported to: chronos_report_example.txt

    [√] OPERATION CHRONOS COMPLETED.

---

## ⚠️ Legal Disclaimer
**Usage of NOEMVEX-WAYBACK for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state, and federal laws. Developers assume no liability.**
**This project is designed for educational purposes and authorized security testing only.**

---

###  Developer
**Emre 'noemvex' Sahin**
*Cybersecurity Specialist & Tool Developer*
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/emresahin-sec) [![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat&logo=github)](https://github.com/noemvex)
