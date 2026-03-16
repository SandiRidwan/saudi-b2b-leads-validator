from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os

# 1. KONFIGURASI LIST (Sangat Penting agar Script Jalan)
CITIES = ["Riyadh", "Jeddah", "Dammam", "Mecca", "Medina", "Al Khobar", "Tabuk", "Abha"]
CATEGORIES = [
    "Construction", "Real Estate", "Trading", "Engineering", 
    "Technology", "Manufacturing", "Logistics", "Medical", 
    "Consulting", "Retail"
]

# 2. CONNECT KE CHROME
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

def saudi_massive_scraper():
    all_leads = []
    file_path = os.path.join(os.path.expanduser("~"), "Desktop", "Master_Data_Saudi.xlsx")
    
    print("--- 🏁 MEMULAI PENYISIRAN NASIONAL ARAB SAUDI ---")

    for city in CITIES:
        for category in CATEGORIES:
            query = f"{category} company in {city}"
            print(f"🔎 Scanning: {query}...")
            
            # Akses Google Maps Langsung
            driver.get(f"https://www.google.com/maps/search/{query.replace(' ', '+')}")
            
            # Tunggu panel feed muncul (max 10 detik)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
            except:
                print(f"   ⚠️ Lewati {query}: Tidak ada hasil atau loading lama.")
                continue

            # --- AUTO SCROLL BRUTAL ---
            # Scroll lebih banyak agar dapat ratusan data per kategori
            for _ in range(8): 
                try:
                    pane = driver.find_element(By.XPATH, '//div[@role="feed"]')
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", pane)
                    time.sleep(1.5)
                except: break

            # --- EXTRACTION ---
            # Selector 'hfpxzc' adalah selector universal untuk link bisnis di Gmaps
            items = driver.find_elements(By.CLASS_NAME, "hfpxzc")
            
            for item in items:
                try:
                    name = item.get_attribute("aria-label")
                    url = item.get_attribute("href")
                    
                    if name and name not in [x['Company Name'] for x in all_leads]:
                        all_leads.append({
                            "Company Name": name,
                            "Industry": category,
                            "City": city,
                            "Gmaps_Link": url,
                            "Website": "Scanning...", # Akan diisi di tahap selanjutnya
                            "Contact Person": "TBA",
                            "Email Address": "TBA"
                        })
                except:
                    continue
            
            # SAVE PROGRES (Real-time ke Desktop)
            if all_leads:
                pd.DataFrame(all_leads).to_excel(file_path, index=False)
                print(f"   ✅ Berhasil Ambil: {len(all_leads)} leads sejauh ini.")

    print(f"\n🏁 SELESAI TOTAL! File tersimpan di Desktop: {file_path}")

# JALANKAN SEKARANG
saudi_massive_scraper()