import time
import numpy as np
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from gsheet_editor import add_rows

def get_data(url):

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)

    # Inisialisasi DataFrame
    df = pd.DataFrame({
        "Nama Program": [],
        "Perusahaan": [],
        "Kota": [],
        "SKS": [],
        "Sistem Belajar": [],
        "Kode": [],
        "Periode": [],
        "Deskripsi": [],
        "Modul Pembelajaran": []
    })

    driver.get(url)

    waitUntil(driver, '//*[@id="root"]/div[5]/div/div/div[2]/div[1]/div/div')
    scroll(driver, '//*[@id="root"]/div[5]/div/div/div[2]/div[1]/div')
    time.sleep(2)
    list_program = driver.find_elements(By.XPATH, '//*[@id="root"]/div[5]/div/div/div[2]/div[1]/div/div/div')

    # membuka program satu per satu untuk membuat halaman program
    time.sleep(2)
    for i, program in enumerate(list_program):
        scroll(driver, '//*[@id="root"]/div[5]/div/div/div[2]/div[1]/div')
        time.sleep(2)
        program.click()

        # halaman program
        time.sleep(2)
        page = driver.find_element(By.XPATH, '//*[@id="root"]/div[5]/div/div/div[2]/div[3]/div[2]/div/div[2]/div[1]')

        # mengambil semua data
        nama_program = page.find_element(By.XPATH, './/div[2]/p[1]').text
        perusahaan = page.find_element(By.XPATH, './/div[2]/p[3]').text
        kota = page.find_element(By.XPATH, './/div[2]/span').text
        sks = page.find_element(By.XPATH, './/div[2]/p[4]').text

        sistem = page.find_element(By.XPATH, 'div[6]/div[2]/p[1]').text

        kode_program = page.find_element(By.XPATH, './/div[7]/div[1]/p[2]').text
        periode_program = page.find_element(By.XPATH, './/div[7]/div[2]/p[2]').text

        rincian = page.find_element(By.XPATH, './/div[9]/p[2]').text

        # time.sleep(1)
        teks_modul = ""
        modul = page.find_elements(By.XPATH, './/div[10]/div')
        for bab in modul:
            teks_modul = teks_modul + bab.text + "\n"

        # tambahkan ke dataframe
        time.sleep(1)
        df = add_rows(df, [nama_program, perusahaan, kota[3:], sks, sistem, kode_program,
                           periode_program, rincian, teks_modul])

        print(f"{i+1}. {nama_program} berhasil ditulis")

    return df

def waitUntil(driver, xpath, timeout=0.5):
    # Tunggu hingga web terbuka sepenuhnya
    try:
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")

def scroll(driver, div):
    # Menemukan elemen div yang ingin di-scroll
    div_element = driver.find_element(By.XPATH, div)

    # Mencari jumlah div yang sudah dimuat
    previous_count = len(div_element.find_elements(By.XPATH, ".//div"))

    # Buat loop yang akan melakukan scroll ke bawah dan menunggu hingga konten baru dimuat
    scrolls = 0  # Jumlah scroll yang telah dilakukan
    max_scrolls = 10  # Jumlah maksimal scroll yang akan dilakukan

    while scrolls < max_scrolls:
        # Scroll ke bawah menggunakan JavaScript Executor
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", div_element)
        time.sleep(1)

        # Cek apakah ada perubahan pada jumlah elemen div setelah melakukan scroll
        current_count = len(div_element.find_elements(By.XPATH, ".//div"))
        if current_count > previous_count:
            previous_count = current_count
            scrolls += 1
        else:
            break