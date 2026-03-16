import pandas as pd
import os

def final_polisher():
    desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    input_path = os.path.join(desktop, "FINAL_DELIVERY_CLIENT.xlsx")
    output_path = os.path.join(desktop, "REPORTS_SAUDI_ACCOUNTING_CLEAN.xlsx")

    if not os.path.exists(input_path):
        print("❌ File FINAL_DELIVERY_CLIENT tidak ditemukan!")
        return

    df = pd.read_excel(input_path)

    # 1. Hapus Duplikat berdasarkan Email agar klien tidak komplain
    df = df.drop_duplicates(subset=['Email Address'], keep='first')

    # 2. Rapikan teks (Huruf Besar di Awal)
    cols_to_fix = ['Company Name', 'City', 'Contact Person']
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = df[col].astype(str).str.title()

    # 3. Pastikan tidak ada nilai 'Nan' yang terlihat jelek
    df = df.replace(['Nan', 'nan', 'None', 'Tba'], 'General Management')

    # 4. Urutkan kolom agar enak dibaca klien
    # Sesuaikan dengan kolom yang kamu punya
    desired_order = [
        'Company Name', 
        'Contact Person', 
        'Email Address', 
        'Website', 
        'City', 
        'Gmaps_Link'
    ]
    
    # Hanya ambil kolom yang memang ada di dataframe
    final_cols = [c for c in desired_order if c in df.columns]
    df = df[final_cols]

    # 5. Simpan ke file final
    df.to_excel(output_path, index=False)
    
    print("-" * 30)
    print(f"🏁 PROJECT SELESAI, SANDI!")
    print(f"Total Data Akurat: {len(df)}")
    print(f"File Siap Dikirim: {output_path}")
    print("-" * 30)

if __name__ == "__main__":
    final_polisher()