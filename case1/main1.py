import time
from auth import auth
from gsheet_editor import update_gsheet
from get_data_from_web import get_data

def main():
    # --- Langkah-langkah untuk memakai program ini
    # Share file Google Sheet ke email Service Account di Google Cloud Project yang telah aktif Google Sheet API dan Google Drive API
    # Copy path keys Service Account pada variabel key_path di bawah
    key_path = 'service-account.json'
    gc = auth(key_path)

    # Buat file Google Sheets
    sheet = gc.create('Program-Program Kampus Merdeka')
    email_anda = 'your.email@example.com'
    sheet.share(email_anda, perm_type='user', role='writer')

    # Buka Worksheet
    worksheet = sheet.worksheet("Sheet1")

    # Web Scraping
    df = get_data('https://kampusmerdeka.kemdikbud.go.id/program/studi-independen/browse/')
    update_gsheet(worksheet, df)
    return

# Function Call
if __name__ == '__main__':
    start = time.time()
    main()
    runtime = time.time() - start
    menit = int(runtime / 60)
    detik = int(runtime % 60)
    print(f"Runtime: {menit} menit {detik} detik")