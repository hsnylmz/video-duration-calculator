import os
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import Scrollbar
from tkinter import ttk
from tkinter import messagebox

# Dil seçeneği
current_language = "en"  # Başlangıçta İngilizce olarak ayarlandı

# Dil çevirileri
translations = {
    "tr": {
        "total_video_duration": "Toplam Video Süresi:",
        "total_video_count": "Toplam Video Sayısı:",
        "folder_label": "Klasör:",
        "video_info_label": "Video Bilgileri:",
        "about_title": "Hakkında",
        "about_text": "Hasan Yılmaz\nEmail: hsnylmz@gmail.com",
        "file_menu": "Dosya",
        "exit_menu": "Çıkış",
        "save_as_menu": "Farklı Kaydet",
        "help_menu": "Yardım",
        "about_menu": "Hakkında",
        "language_menu": "Dil",
        "select_folder_button": "Klasör Seç",
    },
    "en": {
        "total_video_duration": "Total Video Duration:",
        "total_video_count": "Total Video Count:",
        "folder_label": "Folder:",
        "video_info_label": "Video Information:",
        "about_title": "About",
        "about_text": "Hasan Yılmaz\nEmail: hsnylmz@gmail.com",
        "file_menu": "File",
        "exit_menu": "Exit",
        "save_as_menu": "Save As",
        "help_menu": "Help",
        "about_menu": "About",
        "language_menu": "Language",
        "select_folder_button": "Select Folder",
    }
}

# Klasör seçme işlevi
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        result_text.config(state='normal')
        result_text.delete(1.0, 'end')  # Mevcut içeriği temizle
        total_duration, video_count, folder_info = calculate_video_duration(folder_path)
        result_label.config(text=f"{translations[current_language]['total_video_duration']} {format_time(total_duration)}")
        count_label.config(text=f"{translations[current_language]['total_video_count']} {video_count} video")
        for folder_name, duration, video_info in folder_info:
            result_text.insert('end', f"{translations[current_language]['folder_label']} {folder_name} - {translations[current_language]['total_video_duration']} {format_time(duration)}\n")
            result_text.insert('end', f"{translations[current_language]['video_info_label']}:\n")
            for video_name, video_duration in video_info:
                result_text.insert('end', f"- {translations[current_language]['video_info_label']} {video_name} - {translations[current_language]['total_video_duration']} {format_time(video_duration)}\n")
        result_text.config(state='disabled')
        result_text.update_idletasks()  # Metin alanının boyutunu güncelle

# Videoların sürelerini, klasör adlarını ve video isimlerini hesaplayan işlev
def calculate_video_duration(folder_path):
    total_duration = 0
    video_count = 0
    folder_info = []
    supported_formats = (".mp4", ".avi", ".mkv", ".mov", ".flv", ".webm", ".mpeg", ".mpg", ".mxf")  # Desteklenen formatlar
    for root, dirs, files in os.walk(folder_path):
        folder_duration = 0
        video_info = []
        for file in files:
            if file.lower().endswith(supported_formats):
                video_path = os.path.join(root, file)
                cap = cv2.VideoCapture(video_path)
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = frame_count / fps
                total_duration += duration
                folder_duration += duration
                video_count += 1
                video_info.append((file, duration))
                cap.release()
        if folder_duration > 0:
            folder_name = os.path.relpath(root, folder_path)
            folder_info.append((folder_name, folder_duration, video_info))
    return total_duration, video_count, folder_info

# Saniyeyi saat, dakika ve saniyeye dönüştüren işlev
def seconds_to_hms(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

# Süre formatını saat, dakika, saniye olarak dönüştüren işlev
def format_time(seconds):
    hours, minutes, seconds = seconds_to_hms(seconds)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Hakkında penceresini açan işlev
def show_about():
    about_window = tk.Toplevel(root)
    about_window.title(translations[current_language]['about_title'])
    about_window.geometry("300x200")  # Hakkında penceresinin boyutu
    about_label = tk.Label(about_window, text=translations[current_language]['about_text'], padx=20, pady=10)
    about_label.pack()

# Çıkış işlevi
def exit_program():
    root.destroy()

# Farklı Kaydet işlevi
def save_as():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(result_text.get("1.0", tk.END))

# Dil seçeneği değiştiğinde arayüzü güncelle
def change_language(new_language):
    global current_language
    current_language = new_language
    select_button.config(text=translations[current_language]['select_folder_button'])
    file_menu.entryconfig(0, label=translations[current_language]['exit_menu'])
    file_menu.entryconfig(1, label=translations[current_language]['save_as_menu'])
    help_menu.entryconfig(0, label=translations[current_language]['about_menu'])
    language_menu.entryconfig(0, label=translations[current_language]['language_menu'])
    update_interface_language()

# Arayüzdeki metinleri güncelle
def update_interface_language():
    result_label.config(text=translations[current_language]['total_video_duration'])
    count_label.config(text=translations[current_language]['total_video_count'])
    # Diğer metin alanları da burada güncellenebilir

# Arayüzü oluşturma
root = tk.Tk()
root.title("Video Süre Hesaplayıcı")
root.geometry("800x500")  # Pencere boyutunu ayarla

# ttkbootstrap'un "superhero" temasını kullan
style = ttk.Style()
style.configure("TButton", padding=(10, 10), background="#FF6D00")  # Düğme rengi
style.configure("TLabel", padding=(10, 10))  # Etiket rengi
style.map("TButton", background=[("active", "#FF8A3D")])  # Düğme rengi (tıklanınca)

# Menü oluşturma
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=translations[current_language]['file_menu'], menu=file_menu)
file_menu.add_command(label=translations[current_language]['exit_menu'], command=exit_program)
file_menu.add_command(label=translations[current_language]['save_as_menu'], command=save_as)

help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=translations[current_language]['help_menu'], menu=help_menu)
help_menu.add_command(label=translations[current_language]['about_menu'], command=show_about)

language_menu = tk.Menu(help_menu, tearoff=0)
help_menu.add_cascade(label=translations[current_language]['language_menu'], menu=language_menu)
language_menu.add_command(label="Türkçe", command=lambda: change_language("tr"))
language_menu.add_command(label="English", command=lambda: change_language("en"))

select_button = ttk.Button(root, text=translations[current_language]['select_folder_button'], command=select_folder)
select_button.pack(pady=10, side="top")

result_label = ttk.Label(root, text="")
result_label.pack()

count_label = ttk.Label(root, text="")
count_label.pack()

# Scroll çubuğu oluştur
scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")

result_text = tk.Text(root, wrap='word', state='disabled', yscrollcommand=scrollbar.set)
result_text.pack(fill='both', expand=True)  # Metin alanını genişlet

# Scroll çubuğunu metin alanına bağla
scrollbar.config(command=result_text.yview)

# Arayüz dilini güncelleyin
update_interface_language()

root.mainloop()
