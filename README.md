# Preview
## Home
![image](https://github.com/user-attachments/assets/ae8c3de1-c005-4c09-a83b-3007cf882964)

## Detail
![image](https://github.com/user-attachments/assets/35d5fc16-56e1-458c-b342-1645c2d20f77)

# Panduan Instalasi Aplikasi Flask

Panduan ini akan membantu Anda dalam melakukan instalasi dan menjalankan aplikasi Flask beserta semua dependensi yang diperlukan.

## Prasyarat

### 1. Instalasi Python
Pertama, Anda perlu menginstal Python di sistem Anda:

- **Windows**: 
  - Unduh Python dari [python.org](https://python.org)
  - Saat instalasi, pastikan untuk mencentang "Add Python to PATH"

- **Linux**:
```bash
sudo apt update
sudo apt install python3 python3-pip
```

- **macOS**:
```bash
brew install python3
```

## Langkah-langkah Instalasi

### 1. Mengunduh Repository
```bash
git clone https://github.com/78LUKMAN/amicom-simple-anime-recommender.git
cd amicom-simple-anime-recommender
```

### 2. Membuat Virtual Environment
Sangat disarankan untuk membuat virtual environment untuk mengelola dependensi:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalasi Dependensi yang Diperlukan
Setelah virtual environment aktif, install paket-paket yang diperlukan:

```bash
pip install flask
pip install scikit-learn
pip install scipy
pip install pandas
pip install flask-cors
pip install joblib
```

Atau, Anda bisa membuat file `requirements.txt` dengan isi:
```
flask
scikit-learn
scipy
pandas
flask-cors
joblib
```

Kemudian install menggunakan:
```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

1. Pastikan virtual environment Anda sudah aktif
2. Jalankan aplikasi Flask:

```bash
# Windows
cd api
python app.py

# Linux/macOS
cd api
python3 app.py
```

Secara default, aplikasi akan berjalan di `http://localhost:5000`

## Struktur Proyek
Pastikan Anda memiliki semua file yang diperlukan di direktori proyek:
- `app.py` - Aplikasi utama Flask
- File-file model yang diperlukan (file `.npz` untuk matriks sparse)
- File joblib (`.pkl` atau `.joblib`)

## Penyelesaian Masalah

Jika Anda mengalami masalah:

1. Pastikan Python terinstal dengan benar:
```bash
python --version  # atau python3 --version
```

2. Periksa apakah virtual environment sudah aktif (Anda akan melihat `(venv)` di terminal)

3. Konfirmasi semua paket sudah terinstal:
```bash
pip list
```

4. Periksa apakah semua file model dan dataset yang diperlukan ada di direktori yang benar

## Catatan Tambahan

- Pastikan semua file model yang direferensikan di `app.py` berada di lokasi yang benar
- Aplikasi menggunakan CORS, sehingga permintaan cross-origin diizinkan
- Pastikan Anda memiliki ruang disk yang cukup untuk file model dan library yang diperlukan

## Persyaratan Sistem

- Python 3.7 atau lebih tinggi
- RAM yang cukup untuk memuat model dan memproses data
- Ruang disk untuk dependensi dan file model

## Perintah Penting

Berikut adalah ringkasan perintah-perintah penting yang sering digunakan:

```bash
# Mengaktifkan virtual environment
# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Menonaktifkan virtual environment
deactivate

# Menginstal dependensi
pip install -r requirements.txt

# Menjalankan aplikasi
python app.py
```
