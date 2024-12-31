Deskripsi Aplikasi

Aplikasi Penjualan Sepatu adalah aplikasi berbasis GUI (Graphical User Interface) yang memungkinkan pengguna untuk:
1. Menambah, mengedit, dan menghapus produk.
2. Melihat daftar produk lengkap dengan harga yang diformat.
3. Mencatat transaksi penjualan termasuk jumlah produk yang dijual dan total harga.
4. Menampilkan riwayat transaksi dengan detail seperti nama produk, jumlah, total harga, dan tanggal transaksi.
Aplikasi ini dibuat menggunakan Python dengan library tkinter untuk antarmuka pengguna, dan mysql.connector untuk koneksi ke database MySQL.

B. Cara Menjalankan Aplikasi
Prasyarat
Python 3.7 atau lebih baru telah terinstal.
MySQL Server telah terinstal.
Library Python berikut telah terinstal:
mysql.connector
tkinter (terinstal secara bawaan di Python).
Langkah-Langkah
Pastikan MySQL Server berjalan dan database sudah dibuat.
Buat database dengan nama sales_app.
Gunakan struktur tabel yang dijelaskan di bawah ini untuk membuat tabel database.
Simpan kode aplikasi dalam file Python, misalnya sales_app.py.
Jalankan aplikasi menggunakan perintah: python sales_app.py

C. Struktur Tabel Database
Tabel products
Query untuk membuat tabel: 
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL
);

Tabel transactions
Query untuk membuat tabel:
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price FLOAT NOT NULL,
    transaction_date DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
)