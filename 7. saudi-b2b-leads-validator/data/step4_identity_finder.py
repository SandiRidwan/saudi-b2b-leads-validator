from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os

def identity_sniper_free():
    # 1. SETUP PATH
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    input_path = os.path.join(desktop, "CLEAN_100_ACCURATE_SAUDI.xlsx")
    final_path = os.path.join(desktop, "FINAL_DELIVERY_CLIENT.xlsx")

    if not os.path.exists(input_path):
        print(f"❌ File tidak ditemukan: {input_path}")
        return

    # 2. KONEKSI KE CHROME (PORT 9222)
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        # Cek apakah driver benar-benar bisa akses browser
        print(f"✅ Terhubung ke Chrome. Judul Tab: {driver.title}")
    except Exception as e:
        print("❌ GAGAL TERHUBUNG KE CHROME!")
        print("Pastikan Chrome dibuka via CMD dengan port 9222.")
        print(f"Error Detail: {e}")
        return

    # 3. LOAD DATA
    df = pd.read_excel(input_path)
    print(f"--- 🕵️ Sniper Aktif: {len(df)} Perusahaan ---")

    for index, row in df.iterrows():
        # Skip jika sudah ada datanya
        if pd.notnull(row.get('Contact Person')) and row['Contact Person'] not in ["Management Team", "General Manager", "TBA"]:
            continue

        company = str(row['Company Name'])
        city = str(row['City'])
        
        search_query = f'site:linkedin.com/in/ "{company}" "{city}" manager OR owner OR ceo'
        
        try:
            driver.get(f"https://www.google.com/search?q={search_query.replace(' ', '+')}")
            
            # --- CEK CAPTCHA ---
            while "google.com/sorry" in driver.current_url:
                print(f"⚠️ CAPTCHA! Sandi, selesaikan di browser sekarang...")
                time.sleep(5)
            
            time.sleep(4) # Jeda aman

            # --- AMBIL DATA ---
            results = driver.find_elements(By.CSS_SELECTOR, "h3")
            if results:
                first_result = results[0].text
                # Ambil nama sebelum simbol pemisah
                potential_name = re.split(r' - | \| |: ', first_result)[0]
                
                if "LinkedIn" in potential_name or len(potential_name) > 35:
                    res_name = "Management Team"
                else:
                    res_name = potential_name
                
                df.at[index, 'Contact Person'] = res_name
                print(f"✅ [{index+1}] {company} -> {res_name}")
            else:
                df.at[index, 'Contact Person'] = "General Manager"

        except Exception as e:
            print(f"❌ Gagal pada {company}: {e}")
            df.at[index, 'Contact Person'] = "Management Team"

        # Simpan progres tiap 3 data (lebih sering lebih aman)
        if index % 3 == 0:
            df.to_excel(final_path, index=False)

    df.to_excel(final_path, index=False)
    print(f"\n🏁 BERHASIL! File final: {final_path}")

if __name__ == "__main__":
    import re # Import re di sini untuk split logic
    identity_sniper_free()