import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Fungsi teks bergerak (marquee)
def marquee_text(label, window):
    text = label.cget("text")
    label.config(text=text[1:] + text[0])  # Pindahkan karakter pertama ke akhir
    window.after(150, lambda: marquee_text(label, window))  # Ulangi setiap 150ms

# Fungsi untuk membuat koneksi ke database SQLite
def create_connection():
    return sqlite3.connect('hobisiswa.db')

# Fungsi untuk membuat tabel kehadiran siswa jika belum ada
def create_table():
    conn = create_connection()
    c = conn.cursor()
    # Hapus tabel lama jika ada
    c.execute("DROP TABLE IF EXISTS siswa")
    # Buat tabel baru dengan kolom 'hobi'
    c.execute('''CREATE TABLE siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        tanggal TEXT NOT NULL,
        hobi TEXT NOT NULL)''')
    conn.commit()
    conn.close()


# Fungsi untuk menambah data hobi siswa ke database
def insert_data(nama, tanggal, hobi):
    conn = create_connection()
    c = conn.cursor()
    c.execute("INSERT INTO siswa (nama, tanggal, hobi) VALUES (?, ?, ?)", (nama, tanggal, hobi))
    conn.commit()
    conn.close()

# Fungsi untuk mengupdate data hobi siswa
def update_data(id, nama, tanggal, hobi):
    conn = create_connection()
    c = conn.cursor()
    c.execute("UPDATE siswa SET nama = ?, tanggal = ?, hobi = ? WHERE id = ?", (nama, tanggal, hobi, id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data hobi siswa
def delete_data(id):
    conn = create_connection()
    c = conn.cursor()
    c.execute("DELETE FROM siswa WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# Fungsi untuk mencari siswa berdasarkan nama
def search_data(keyword):
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM siswa WHERE nama LIKE ?", ('%' + keyword + '%',))
    result = c.fetchall()
    conn.close()
    return result

# Fungsi untuk mengambil semua data siswa
def get_all_data():
    conn = create_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM siswa")
    result = c.fetchall()
    conn.close()
    return result

# Fungsi untuk menambah data
def tambah_data():
    nama = entry_nama.get()
    tanggal = entry_tanggal.get()
    hobi = combo_hobi.get()
    
    if not nama or not tanggal or not hobi:
        messagebox.showwarning("Input Error", "Semua kolom harus diisi!")
        return
    
    insert_data(nama, tanggal, hobi)
    messagebox.showinfo("Sukses", "Data berhasil ditambahkan!")
    tampilkan_data()

# Fungsi untuk mengupdate data
def ubah_data():
    try:
        selected_item = treeview.selection()[0]
        id_siswa = treeview.item(selected_item)['values'][0]
        nama = entry_nama.get()
        tanggal = entry_tanggal.get()
        hobi = combo_hobi.get()
        
        if not nama or not tanggal or not hobi:
            messagebox.showwarning("Input Error", "Semua kolom harus diisi!")
            return
        
        update_data(id_siswa, nama, tanggal, hobi)
        messagebox.showinfo("Sukses", "Data berhasil diubah!")
        tampilkan_data()
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin diubah!")

# Fungsi untuk menghapus data
def hapus_data():
    try:
        selected_item = treeview.selection()[0]
        id_siswa = treeview.item(selected_item)['values'][0]
        delete_data(id_siswa)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        tampilkan_data()
    except IndexError:
        messagebox.showwarning("Pilih Data", "Pilih data yang ingin dihapus!")

# Fungsi untuk mencari data
def cari_data():
    keyword = entry_cari.get()
    hasil = search_data(keyword)
    tampilkan_data(hasil)

# Fungsi untuk menampilkan data ke Treeview
def tampilkan_data(data=None):
    for row in treeview.get_children():
        treeview.delete(row)
    
    if data is None:
        data = get_all_data()
    
    for row in data:
        treeview.insert("", "end", values=row)

# Fungsi untuk login
def login():
    valid_username = "aku"
    valid_password = "gtg"
    
    username = entry_email_login.get()
    password = entry_password_login.get()
    
    if username == valid_username and password == valid_password:
        messagebox.showinfo("Login Sukses", "Berhasil login!")
        login_window.withdraw()
        main_window.deiconify()
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah!")

# Fungsi untuk logout
def logout():
    main_window.withdraw()
    login_window.deiconify()
    entry_email_login.delete(0, tk.END)
    entry_password_login.delete(0, tk.END)

# Buat jendela login
login_window = tk.Tk()
login_window.title("Login Aplikasi Pendataan Hobi Siswa")
login_window.geometry("400x300")
login_window.configure(bg="#DE73FF")

tk.Label(login_window, text="Login", font=("Helvetica", 20, "bold"), bg="#6F2DA8", fg="#FFFFFF").pack(pady=20)
tk.Label(login_window, text="Username", font=("Helvetica", 12), bg="#6F2DA8", fg="#FFFFFF").pack()
entry_email_login = tk.Entry(login_window, font=("Helvetica", 12), width=30)
entry_email_login.pack(pady=5)
tk.Label(login_window, text="Password", font=("Helvetica", 12), bg="#6F2DA8", fg="#FFFFFF").pack()
entry_password_login = tk.Entry(login_window, font=("Helvetica", 12), width=30, show="*")
entry_password_login.pack(pady=5)
tk.Button(login_window, text="Login", command=login, font=("Helvetica", 12, "bold"), bg="#6F2DA8", fg="#FFFFFF").pack(pady=20)

# Buat jendela utama
main_window = tk.Tk()
main_window.title("Aplikasi Pendataan Hobi Siswa")
main_window.geometry("600x700")
main_window.configure(bg="#DE73FF")
main_window.withdraw()

header_frame = tk.Frame(main_window, bg="#8F00FF", height=250)
header_frame.pack(fill=tk.X)
marquee_label = tk.Label(header_frame, text="Selamat Datang di Aplikasi Pendataan Hobi Siswa! ", font=("Helvetica", 75), bg="#8F00FF", fg="#FFFFFF")
marquee_label.pack(expand=True)
marquee_text(marquee_label, main_window)

btn_logout = tk.Button(main_window, text="Logout", command=logout, font=("Helvetica", 12, "bold"), bg="#6F2DA8", fg="#FFFFFF")
btn_logout.pack(pady=5)

# Form input
form_frame = tk.Frame(main_window, bg="#F0F0F0")
form_frame.pack(pady=10)
tk.Label(form_frame, text="Nama", font=("Helvetica", 12), bg="#F0F0F0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_nama = tk.Entry(form_frame, font=("Helvetica", 12))
entry_nama.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Tanggal (YYYY-MM-DD)", font=("Helvetica", 12), bg="#F0F0F0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_tanggal = tk.Entry(form_frame, font=("Helvetica", 12))
entry_tanggal.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Hobi", font=("Helvetica", 12), bg="#F0F0F0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
combo_hobi = ttk.Combobox(form_frame, values=["Pramuka", "Paskibra", "Basket", "Voli"], font=("Helvetica", 12))
combo_hobi.grid(row=2, column=1, padx=10, pady=5)

btn_tambah = ttk.Button(main_window, text="Tambah", command=tambah_data)
btn_tambah.pack(pady=5)
btn_ubah = ttk.Button(main_window, text="Ubah", command=ubah_data)
btn_ubah.pack(pady=5)
btn_hapus = ttk.Button(main_window, text="Hapus", command=hapus_data)
btn_hapus.pack(pady=5)

frame_cari = tk.Frame(main_window, bg="#F0F0F0")
frame_cari.pack(pady=10)
tk.Label(frame_cari, text="Cari Nama:", font=("Helvetica", 12), bg="#F0F0F0").grid(row=0, column=0, padx=5, pady=5)
entry_cari = tk.Entry(frame_cari, font=("Helvetica", 12))
entry_cari.grid(row=0, column=1, padx=5, pady=5)
btn_cari = ttk.Button(frame_cari, text="Cari", command=cari_data)
btn_cari.grid(row=0, column=2, padx=5, pady=5)

treeview = ttk.Treeview(main_window, columns=("ID", "Nama", "Tanggal", "Hobi"), show="headings", style="Treeview")
treeview.pack(pady=10)
treeview.heading("ID", text="ID")
treeview.heading("Nama", text="Nama")
treeview.heading("Tanggal", text="Tanggal")
treeview.heading("Hobi", text="Hobi")
treeview.column("ID", width=50)
treeview.column("Nama", width=200)
treeview.column("Tanggal", width=100)
treeview.column("Hobi", width=100)

create_table()
tampilkan_data()
login_window.mainloop()
