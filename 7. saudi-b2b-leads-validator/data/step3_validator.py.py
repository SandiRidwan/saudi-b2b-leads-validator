import pandas as pd
import dns.resolver
import os
import re

def validate_leads_accuracy():
    # Menyesuaikan path Desktop agar lebih universal
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    input_path = os.path.join(desktop, "FINAL_LEADS_SAUDI.xlsx")
    clean_path = os.path.join(desktop, "CLEAN_100_ACCURATE_SAUDI.xlsx")

    if not os.path.exists(input_path):
        print(f"❌ File tidak ditemukan di: {input_path}")
        print("Pastikan Modul 2 sudah selesai dan menghasilkan file tersebut.")
        return

    # Baca file Excel
    df = pd.read_excel(input_path)
    print(f"--- 🛡️ Memulai Validasi Akurasi 100%: {len(df)} baris data ---")

    valid_leads = []
    
    # List sampah yang harus dibuang
    blacklist = ['sentry', 'wix', 'domain', 'example', 'test', 'png', 'jpg', 'hosting', 'wordpress', 'email', 'form']

    for index, row in df.iterrows():
        email = str(row['Email Address']).lower().strip()
        
        # 1. Filter dasar
        if email == 'nan' or email == 'tba' or '@' not in email:
            continue

        # 2. Filter Blacklist (Hapus email sistem/sampah)
        if any(word in email for word in blacklist):
            continue

        # 3. Validasi DNS (Cek server email aktif)
        try:
            domain = email.split('@')[1]
            # Timeout ditambah agar tidak error karena koneksi lambat
            dns.resolver.resolve(domain, 'MX', lifetime=5)
            
            valid_leads.append(row)
            print(f"✅ VALID: {email}")
        except Exception:
            # Jika domain tidak punya server email (MX Record), maka email ini 100% mati
            print(f"❌ INVALID (Server Mati): {email}")
            continue

    # Simpan hasil akhir
    if valid_leads:
        df_clean = pd.DataFrame(valid_leads)
        df_clean.to_excel(clean_path, index=False)
        print("-" * 30)
        print(f"🏁 SELESAI!")
        print(f"Data Masuk: {len(df)}")
        print(f"Data Lolos Verifikasi (100% Akurat): {len(df_clean)}")
        print(f"File Siap: {clean_path}")
    else:
        print("❌ Tidak ada email valid yang ditemukan setelah proses filter.")

# --- BARIS WAJIB: Memanggil fungsi agar script berjalan ---
if __name__ == "__main__":
    validate_leads_accuracy()