# TechSpark E-commerce Project

Proyek ini adalah platform e-commerce yang dibangun menggunakan Django. Fitur-fitur utama meliputi manajemen produk, keranjang belanja, proses checkout, dan riwayat pesanan.

## Setup Proyek

Untuk menjalankan proyek ini secara lokal:

1.  **Clone repositori:**
    ```bash
    git clone <URL_REPOSITORI_ANDA>
    cd MYWEB
    ```
2.  **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
3.  **Instal dependensi:**
    ```bash
    pip install -r requirements.txt # (Asumsi ada file requirements.txt, jika tidak, instal Django, dll. secara manual)
    ```
4.  **Migrasi database:**
    ```bash
    python manage.py migrate
    ```
5.  **Buat superuser (opsional):
    ```bash
    python manage.py createsuperuser
    ```
6.  **Jalankan server pengembangan:**
    ```bash
    python manage.py runserver
    ```

Aplikasi akan tersedia di `http://127.0.0.1:8000/`.

## Struktur Proyek

-   `config/`: Pengaturan proyek Django utama.
-   `techspark/`: Aplikasi utama e-commerce yang berisi model, view, URL, dan template.
-   `static/`: File statis (CSS, JS, gambar).
-   `templates/`: Template HTML untuk aplikasi.

## Pembuat Proyek

| Nama Lengkap      | NIM         |
| :---------------- | :---------- |
| [Nama Anggota 1] | [NIM Anggota 1] |
| [Nama Anggota 2] | [NIM Anggota 2] |
| [Nama Anggota 3] | [NIM Anggota 3] |
| [Nama Anggota 4] | [NIM Anggota 4] |
