import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import os

# 1. CONNECT KE CHROME
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

def email_sniper_module():
    file_path = os.path.join(os.path.expanduser("~"), "Desktop", "Master_Data_Saudi.xlsx")
    output_path = os.path.join(os.path.expanduser("~"), "Desktop", "FINAL_LEADS_SAUDI.xlsx")

    if not os.path.exists(file_path):
        print("❌ Error: File Master_Data_Saudi.xlsx tidak ditemukan di Desktop!")
        return

    df = pd.read_excel(file_path)
    print(f"--- 🚀 Memulai Deep Scan untuk {len(df)} data ---")

    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    for index, row in df.iterrows():
        # Lewati jika sudah ada emailnya
        if pd.notnull(row.get('Email Address')) and row['Email Address'] != "TBA":
            continue

        gmaps_link = row['Gmaps_Link']
        print(f"[{index+1}/{len(df)}] Meneliti: {row['Company Name']}")

        try:
            driver.get(gmaps_link)
            time.sleep(4)

            # --- TAHAP A: CARI WEBSITE DARI GMAPS ---
            website_url = ""
            try:
                # Mencari elemen yang punya data-item-id="authority" (biasanya website di Gmaps)
                web_element = driver.find_element(By.CSS_SELECTOR, 'a[data-item-id="authority"]')
                website_url = web_element.get_attribute('href')
                df.at[index, 'Website'] = website_url
            except:
                df.at[index, 'Website'] = "None"

            # --- TAHAP B: MASUK KE WEBSITE & CARI EMAIL ---
            if website_url:
                driver.get(website_url)
                time.sleep(5)
                
                # Scan seluruh teks di halaman utama
                page_source = driver.page_source
                emails = re.findall(email_pattern, page_source)
                
                # Jika tidak ketemu di depan, coba cari link "Contact"
                if not emails:
                    try:
                        contact_link = driver.find_element(By.PARTIAL_LINK_TEXT, "Contact").get_attribute('href')
                        driver.get(contact_link)
                        time.sleep(3)
                        emails = re.findall(email_pattern, driver.page_source)
                    except: pass

                if emails:
                    # Ambil email pertama yang unik (abaikan gambar/png/jpg)
                    valid_emails = [e for e in emails if not e.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                    if valid_emails:
                        found_email = list(set(valid_emails))[0]
                        df.at[index, 'Email Address'] = found_email
                        print(f"   🔥 DAPAT EMAIL: {found_email}")

        except Exception as e:
            print(f"   ⚠️ Skip: {e}")

        # Simpan progres setiap 5 data agar aman
        if index % 5 == 0:
            df.to_excel(output_path, index=False)

    df.to_excel(output_path, index=False)
    print(f"🏁 SELESAI! Hasil akhir ada di: {output_path}")

# JALANKAN
email_sniper_module()