import customtkinter as ctk
from ui.adminPage import AdminSayfasi
from ui.loginPage import LoginPage
from ui.customerPage import MusteriSayfasi
from manager.data_manager import Data_Manager

if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Araç Kiralama Sistemi")
    root.geometry("1100x750")
    
    db=Data_Manager()

    #Proje Çalışınca Açılacak Sayfa
    app = LoginPage(parent=root, controller=None,db_manager=db)
    app.grid(row=0, column=0, sticky="nsew")

    # Grid ayarları 
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Uygulamayı başlat
    root.mainloop()