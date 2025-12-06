import customtkinter as ctk
from tkinter import messagebox

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#ECF0F1")
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #giriş kutusu
        self.login_frame = ctk.CTkFrame(
            self,
            width=350,
            corner_radius=15,
            fg_color="2C3E50"
        )
        self.login_frame.grid(row=0, column=0, padx=20, pady=20)

        #giriş kutusundaki elemanların ortalanması
        self.login_frame.grid_columnconfigure(0, weight=1)

        #Labellar
        self.lbl_welcome = ctk.CTkLabel(
            self.login_frame,
            text="Hoş Geldiniz",
            font=("Roboto", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.lbl_welcome.grid(row=0, column=0, padx=20, pady=(40, 5))

        self.lbl_subtitle = ctk.CTkLabel(
            self.login_frame,
            text="Hesabınıza Giriş Yapınız",
            font=("Roboto", 14),
            text_color="#FFFFFF"
        )
        self.lbl_subtitle.grid(row=1, column=0, padx=20, pady=(0,30))

        #E-mail Giriş Alanı
        self.entry_email = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Email",
            font=("Roboto", 14),
            width=250,
            height=40,
        )
        self.entry_email.grid(row=2, column=0, padx=20, pady=10)

        #Şifre Giriş Alanı
        self.entry_password = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Şifre",
            font=("Roboto", 14),
            width=250,
            height=40,
            show="*"
        )
        self.entry_password.grid(row=3, column=0, padx=20, pady=10)

        #Giriş Butonu
        self.btn_login = ctk.CTkButton(
            self.login_frame,
            text="Giriş Yap",
            font=("Roboto", 14,"bold"),
            fg_color="1ABC9C",
            hover_color="#16A085", #üstüne gelince koyulaştırıyor
            width=250,
            height=40,
            corner_radius=8,
            command=self.login_event
        )
        self.btn_login.grid(row=4, column=0, padx=20, pady=(30, 15))

        #kayıt ol linki
        self.btn_register_text = ctk.CTkButton(
            self.login_frame,
            text="Hesabın yok mu? Kayıt ol",
            fg_color="transparent",
            text_color="#BDC3C7",
            hover_color="#2C3E50",
            width=250,
            height=30,
            font=("Roboto", 12),
            cursor="hand2",
            command=self.go_to_register
        )
        self.btn_register_text.grid(row=5, column=0, padx=20, pady=(0, 30))

        def login_event(self):
            print("login event")

        def go_to_register(self):
            print("Registera giden fonksiyon")