import tkinter as tk
from tkinter import ttk, messagebox
from textdistance import levenshtein

def cari_kata_mirip(kata):
    kata_terdekat = ""
    jarak_terdekat = float('inf')

    for kata_baku in kata_baku_list:
        jarak = levenshtein.normalized_similarity(kata, kata_baku)
        if jarak > 0.6 and jarak < jarak_terdekat:
            jarak_terdekat = jarak
            kata_terdekat = kata_baku

    return kata_terdekat

def perbaiki_kata_baku():
    # Mendapatkan kata dari input pengguna, membersihkannya, dan mengonversi ke huruf kecil
    kata = kata_entry.get("1.0", "end-1c").strip().lower()
    if kata in kata_baku_list:
        # Jika kata ada dalam daftar kata baku, tampilkan pesan sesuai
        hasil_label.config(text=f'Kata "{kata}" merupakan kata baku sesuai pada database kami.', fg="#00A86B")
    else:
        kata_mirip = cari_kata_mirip(kata)
        if kata_mirip:
            # Jika kata tidak ada dalam database dan ada kata mirip, tampilkan kata mirip
            hasil_label.config(text=f'Kata "{kata}" tidak ditemukan dalam database kami. Apakah Anda maksud: "{kata_mirip}"?', fg="#FBC02D")
        else:
            # Jika kata tidak ada dalam database dan tidak ada kata mirip, tampilkan pesan kesalahan
            pesan_kesalahan = f'Kata "{kata}" tidak ditemukan dalam database kami. Coba periksa dan perbaiki kata Anda.\n\n'
            pesan_kesalahan += f'Anda bisa mencari kata tersebut di KBBI melalui tautan berikut:\nhttp://kbbi.kemdikbud.go.id/entri/{kata}'
            hasil_label.config(text=pesan_kesalahan, fg="#E74C3C")
            messagebox.showinfo("Kata Tidak Ditemukan", pesan_kesalahan)
            kata_terdekat = cari_kata_mirip(kata)
            if kata_terdekat:
                # Jika ada kata terdekat, gantilah input pengguna dengan kata terdekat
                kata_entry.delete("1.0", "end-1c")
                kata_entry.insert("1.0", kata_terdekat)

with open('kata_baku.csv', 'r') as file:
    kata_baku_list = [kata.strip().lower() for kata in file.readlines()]

def tampilkan_halaman_about(event):
    about_text = """
Cek Kata Baku

Versi 1.0

Tentang Aplikasi:
Aplikasi "Cek Kata Baku" adalah sebuah alat sederhana yang dirancang untuk membantu pengguna dalam memeriksa apakah sebuah kata tertentu merupakan kata baku dalam bahasa Indonesia. Aplikasi ini sangat berguna untuk pengecekan cepat dan perbaikan kata-kata dalam bahasa Indonesia.

Terima kasih atas dukungan Anda!

Dikembangkan oleh: Andry Syva Maldini
Email   : andrymldni@gmail.com
LinkedIn: linkedin.com/in/andrymldni

© 2023, Cek Kata Baku."""

    about_textbox.config(state=tk.NORMAL)  # Aktifkan mode pengeditan
    about_textbox.delete(1.0, tk.END)  # Hapus teks sebelum menampilkan informasi "About"
    about_textbox.insert(tk.END, about_text)  # Tampilkan informasi "About"
    about_textbox.config(state=tk.DISABLED)  # Nonaktifkan mode pengeditan

root = tk.Tk()
root.title("Kata Baku")
root.geometry("600x410")

# Membuat tab "Home" dan "About"
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand='yes')

home_frame = ttk.Frame(notebook)
about_frame = ttk.Frame(notebook)

notebook.add(home_frame, text='Home')
notebook.add(about_frame, text='About')

judul_label = tk.Label(home_frame, text="Cek Kata Baku", font=("Poppins", 20, "bold"), fg="#00A86B")
judul_label.pack(pady=20)

kata_label = tk.Label(home_frame, text="Masukkan kata:", font=("Poppins", 14))
kata_label.pack()

kata_entry = tk.Text(home_frame, height=1, width=45, font=("Poppins", 12))
kata_entry.pack()

cek_button = tk.Button(home_frame, text="Cek Kata", command=perbaiki_kata_baku, font=("Poppins", 13), bg="#00A86B", fg="#FFFFFF", relief=tk.RAISED, borderwidth=2, padx=10, pady=5)
cek_button.pack(pady=20)

hasil_label = tk.Label(home_frame, text="", font=("Poppins", 12), wraplength=300)
hasil_label.pack()

about_textbox = tk.Text(about_frame, font=("Poppins", 12), wrap=tk.WORD, state=tk.DISABLED)  # Tambahkan state=tk.DISABLED
about_textbox.pack(padx=20, pady=20)

# Event binding untuk tab "Tentang" agar menampilkan informasi "Tentang"
notebook.bind("<<NotebookTabChanged>>", tampilkan_halaman_about)

root.mainloop()