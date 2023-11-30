import datetime
import maskpass

from Google import Create_Service, create_calendar_event, send_invitation_email

# Catatan:
# Simpan file credentials.json di folder yang sama dengan file python ini
# Untuk mengirim email dengan python ini, pastikan email pengirim mengaktifkan
# "Akses aplikasi yang kurang aman"

def main():
    # Lokasi file JSON kredensial
    credentials_file = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    service = Create_Service(credentials_file, 'calendar', 'v3', SCOPES)

    # Set info event
    summary = 'Undangan Mabar Futsal'
    start_time = datetime.datetime.now() + datetime.timedelta(hours=12, minutes=2)  # Pelaksanaan 12 jam dari sekarang
    duration = 120  # Durasi 2 jam (120 menit)
    attendees = ['z@gmail.com', 'z@gmail.com']
    location = 'Mayasari Futsal Cibiru'

    # Setting email
    # Aktifkan "Akses aplikasi yang kurang aman" pada email pengirm
    print()
    sender = input("Email Pengirim: ")
    pw = maskpass.askpass("Password Pengirim: ")
    recipients = attendees
    subject = 'Undangan Mabar Futsal'

    # Buat event di Google Calendar
    create_calendar_event(service, summary, start_time, duration, location, attendees)
    
    # Mengambil informasi acara dari objek event
    desc = 'Hai Guys. Untuk mempererat silaturahmi dan membuat badan tetap sehat dan bugar, yuk ikut mabar futsal yang akan dilaksanakan pada:'

    # Menyusun konten email dengan informasi acara
    email_body = f"""{desc} \n\nWaktu: {start_time} \nLokasi: {location}"""

    # Kirim email
    send_invitation_email(sender, pw, recipients,
                          subject, email_body)

if __name__ == '__main__':
    main()
