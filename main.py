import customtkinter as ctk
from ui.adminPage import AdminSayfasi

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Araç Kiralama Sistemi")
    root.geometry("1100x750")

    #Proje Çalışınca Açılacak Sayfa
    app = AdminSayfasi(parent=root, controller=None)
    app.grid(row=0, column=0, sticky="nsew")

    # Grid ayarları 
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Uygulamayı başlat
    root.mainloop()