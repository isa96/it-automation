from datetime import datetime
import time
import schedule

import sys

from Google import Create_Service

def main():
    # Konfigurasi Google Sheets API
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SPREADSHEET_ID = '1JSgfzgXzJ3zYwITGuBiHlCh56GZUE0uLV-vGBrVTS4Q'
    RANGE_NAME = 'Sheet1!A:C'

    # Membuat koneksi ke Google Sheets API
    service = Create_Service('credentials.json', 'sheets', 'v4', SCOPES)
    sheet = service.spreadsheets()

    # Fungsi untuk memperbarui nilai dan waktu terakhir diupdate
    def update_values():
        # Mendapatkan data dari spreadsheet
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        # Melengkapi nilai kosong dengan None
        for row in values:
            if len(row) < 3:
                row.append(None)

        # Loop melalui semua baris, dimulai dari baris kedua
        for i in range(1, len(values)):
            # Mendapatkan nilai saat ini
            current_value = int(values[i][1])

            # Menambahkan 1 pada nilai
            updated_value = current_value + 1

            # Mendapatkan waktu sekarang
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Memperbarui nilai dan waktu terakhir diupdate
            values[i][1] = str(updated_value)
            values[i][2] = current_time

            # Mengirim perintah update ke Google Sheets API
            update_body = {
                'values': [[values[i][1], values[i][2]]]
            }
            sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                                  range=f'Sheet1!B{i+1}:C{i+1}',
                                  valueInputOption='RAW',
                                  body=update_body).execute()

            # Delay selama 3 detik
            time.sleep(3)

    # Fungsi untuk menjalankan rutinitas setiap 10 menit
    def run_scheduler():
        print("Update dimulai...")
        update_values()

    # Konfigurasi scheduler
    schedule.every(10).minutes.do(run_scheduler)

    # Loop untuk menjalankan scheduler secara terus-menerus
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()