import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

# Fungsi untuk menghubungkan ke database
def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sales_app"
    )

# Fungsi untuk memformat angka dengan titik sebagai pemisah ribuan
def format_price(price):
    if price.isdigit():
        return f"{int(price):,}".replace(",", ".")
    return price

# Fungsi untuk memperbarui input harga secara otomatis dengan format ribuan
def update_price_format(event):
    current_text = entry_price.get()
    clean_text = ''.join(filter(str.isdigit, current_text))
    formatted_text = format_price(clean_text)
    entry_price.delete(0, tk.END)
    entry_price.insert(0, formatted_text)

# Fungsi untuk menambahkan produk
def add_product():
    product_name = entry_name.get()
    product_price = entry_price.get().replace(".", "")

    if not (product_name and product_price):
        messagebox.showerror("Error", "Semua kolom harus diisi!")
        return

    try:
        product_price = float(product_price)
    except ValueError:
        messagebox.showerror("Error", "Harga harus berupa angka!")
        return

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (product_name, product_price))
    conn.commit()
    cursor.close()
    conn.close()

    update_table()
    update_product_dropdown()
    clear_entries()
    messagebox.showinfo("Sukses", "Produk berhasil ditambahkan!")

# Fungsi untuk menghapus produk
def delete_product():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang ingin dihapus!")
        return

    product_id = table.item(selected_item[0], "values")[0]

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()

    update_table()
    update_product_dropdown()
    messagebox.showinfo("Sukses", "Produk berhasil dihapus!")

# Fungsi untuk mengedit produk
def edit_product():
    selected_item = table.selection()
    if not selected_item:
        messagebox.showerror("Error", "Pilih produk yang ingin diedit!")
        return

    product_id = table.item(selected_item[0], "values")[0]
    new_name = entry_name.get()
    new_price = entry_price.get().replace(".", "")

    if not (new_name and new_price):
        messagebox.showerror("Error", "Semua kolom harus diisi untuk mengedit produk!")
        return

    try:
        new_price = float(new_price)
    except ValueError:
        messagebox.showerror("Error", "Harga harus berupa angka!")
        return

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (new_name, new_price, product_id))
    conn.commit()
    cursor.close()
    conn.close()

    update_table()
    update_product_dropdown()
    clear_entries()
    messagebox.showinfo("Sukses", "Produk berhasil diperbarui!")

# Fungsi untuk memperbarui tabel produk
def update_table():
    for row in table.get_children():
        table.delete(row)

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in rows:
        formatted_price = f"{int(row[2]):,}".replace(",", ".")
        table.insert("", "end", values=(row[0], row[1], formatted_price))

# Fungsi untuk memperbarui dropdown produk
def update_product_dropdown():
    dropdown_menu['values'] = []
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM products")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    product_dict.clear()
    for row in rows:
        product_dict[row[1]] = row[0]
    dropdown_menu['values'] = list(product_dict.keys())

# Fungsi untuk mencatat transaksi
def record_transaction():
    product_name = selected_product.get()
    quantity = entry_quantity.get()

    if not (product_name and quantity):
        messagebox.showerror("Error", "Semua kolom harus diisi!")
        return

    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Error", "Jumlah harus berupa angka!")
        return

    product_id = product_dict.get(product_name)

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
    product_price = cursor.fetchone()[0]

    total_price = quantity * product_price
    transaction_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO transactions (product_id, quantity, total_price, transaction_date) VALUES (%s, %s, %s, %s)",
        (product_id, quantity, total_price, transaction_date)
    )
    conn.commit()
    cursor.close()
    conn.close()

    update_transaction_table()
    clear_transaction_entries()
    messagebox.showinfo("Sukses", "Transaksi berhasil dicatat!")

# Fungsi untuk memperbarui tabel transaksi
def update_transaction_table():
    for row in transaction_table.get_children():
        transaction_table.delete(row)

    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT transactions.id, products.name, transactions.quantity, transactions.total_price, transactions.transaction_date
        FROM transactions
        JOIN products ON transactions.product_id = products.id
    ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in rows:
        formatted_total_price = f"{int(row[3]):,}".replace(",", ".")
        transaction_table.insert("", "end", values=(row[0], row[1], row[2], formatted_total_price, row[4]))

# Fungsi untuk membersihkan input transaksi
def clear_transaction_entries():
    selected_product.set("")
    entry_quantity.delete(0, tk.END)

# Fungsi untuk membersihkan input produk
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# GUI
root = tk.Tk()
root.title("Aplikasi Penjualan Sepatu")
root.geometry("900x600")

product_dict = {}

# Frame Input Produk
frame_input = tk.Frame(root)
frame_input.pack(pady=10)

tk.Label(frame_input, text="Nama Produk:").grid(row=0, column=0, padx=5, pady=5)
entry_name = tk.Entry(frame_input)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Harga Produk:").grid(row=1, column=0, padx=5, pady=5)
entry_price = tk.Entry(frame_input)
entry_price.grid(row=1, column=1, padx=5, pady=5)
entry_price.bind("<KeyRelease>", update_price_format)

tk.Button(frame_input, text="Tambah Produk", command=add_product).grid(row=2, column=0, pady=10)
tk.Button(frame_input, text="Edit Produk", command=edit_product).grid(row=2, column=1, pady=10)
tk.Button(frame_input, text="Hapus Produk", command=delete_product).grid(row=2, column=2, pady=10)

# Tabel Produk
table = ttk.Treeview(root, columns=("ID", "Nama", "Harga"), show="headings")
table.heading("ID", text="ID Produk")
table.heading("Nama", text="Nama Produk")
table.heading("Harga", text="Harga Produk")
table.pack(fill=tk.BOTH, expand=True, pady=10)

# Frame Transaksi
frame_transaction = tk.Frame(root)
frame_transaction.pack(pady=10)

tk.Label(frame_transaction, text="Pilih Produk:").grid(row=0, column=0, padx=5, pady=5)
selected_product = tk.StringVar()
dropdown_menu = ttk.Combobox(frame_transaction, textvariable=selected_product)
dropdown_menu.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_transaction, text="Jumlah:").grid(row=1, column=0, padx=5, pady=5)
entry_quantity = tk.Entry(frame_transaction)
entry_quantity.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame_transaction, text="Catat Transaksi", command=record_transaction).grid(row=2, column=0, columnspan=2, pady=10)

# Tabel Transaksi
transaction_table = ttk.Treeview(root, columns=("ID", "Nama Produk", "Jumlah", "Total Harga", "Tanggal"), show="headings")
transaction_table.heading("ID", text="ID Transaksi")
transaction_table.heading("Nama Produk", text="Nama Produk")
transaction_table.heading("Jumlah", text="Jumlah")
transaction_table.heading("Total Harga", text="Total Harga")
transaction_table.heading("Tanggal", text="Tanggal Transaksi")
transaction_table.pack(fill=tk.BOTH, expand=True, pady=10)

# Inisialisasi GUI
update_table()
update_product_dropdown()
update_transaction_table()

# Menjalankan aplikasi
root.mainloop()
