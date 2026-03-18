# 🇸🇦 Saudi Arabia Leads Sniper & Validator
**High-Precision B2B Prospecting & OSINT Identity Matching Engine**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Automation-Selenium-red.svg?style=for-the-badge&logo=selenium)
![OSINT](https://img.shields.io/badge/Field-OSINT-black.svg?style=for-the-badge)
![Market](https://img.shields.io/badge/Market-Saudi_Arabia-green.svg?style=for-the-badge)

---

## 🎯 Project Overview
A sophisticated automation suite designed to penetrate the **Saudi Arabian B2B market**. This isn't just a scraper; it's a "Sniper" that identifies high-level decision-makers (CEOs, Managers, Directors) using advanced OSINT techniques and validates their contact points with 100% accuracy.

> **Targeting:** Construction, Oil & Gas, Tech Startups, and Retail across Riyadh, Jeddah, and Dammam.

---

## ⚡ The Sniper Modules

### 📍 Module 1 & 2: The Harvester (Maps & Web)
* **Deep Scrape:** Extracts business entities from **Google Maps** with localized Arabic/English keyword support.
* **Domain Discovery:** Automatically identifies official corporate websites and extracts metadata.

### 🛡️ Module 3: The Validator (DNS/MX)
* Uses `DNSPython` to perform **Real-time MX-Record verification**.
* Eliminates "Catch-all" domains and ensures **100% email deliverability** to protect your sender reputation.

### 🎯 Module 4: Identity Sniper (OSINT Matching)
* **Dorking Engine:** Implements Google/Bing/DuckDuckGo Dorking to find specific LinkedIn profiles of decision-makers.
* **Role Identification:** Matches company names with "CEO", "Owner", or "Procurement Manager" tags.

### 🕵️ Module 5: Stealth Logic (Anti-Bot)
* **Human-Mimicry:** Randomized delays and mouse movement simulation.
* **Search Fallback:** Automatically switches between search engines (Bing/DuckDuckGo) when bot detection is triggered.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.x |
| **Browser Engine** | Selenium WebDriver |
| **Data Engine** | Pandas (Dataframes & CSV Processing) |
| **Network** | DNSPython (MX Record Validation) |
| **Stealth** | Remote Debugging & Custom User-Agents |

---

## ⚙️ Setup & Execution

### 1️⃣ Chrome Remote Debugging
To bypass advanced bot detection, run Chrome in remote debugging mode:
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\sel_profile"
