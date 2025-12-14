import customtkinter as ctk
from tkinter import messagebox


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller, db_manager):
        super().__init__(parent, fg_color="#ECF0F1")
        self.controller = controller
        self.db=db_manager

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #Kayıt kutusu
        self.register_frame=ctk.CTkFrame(
            self,
            width=400,
            corner_radius=15,
            fg_color="#2C3E50"
        )
        self.register_frame.grid(row=0, column=0, padx=20, pady=20)

        # Kart içi grid ayarları (2 Sütunlu yapı için)
        self.register_frame.grid_columnconfigure((0, 1), weight=1)

        #hesap oluştur yazısı
        self.lbl_title=ctk.CTkLabel(
            self.register_frame,
            text="HESAP OLUŞTUR",
            font=("Roboto", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.lbl_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(30, 5))

        # 1. Satır: Ad ve Soyad (Yan Yana)
        self.entry_ad = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="Ad",
            width=160,
            height=40,
            font=("Roboto", 14)
        )
        self.entry_ad.grid(row=2, column=0, padx=(20, 10), pady=10)
        self.entry_ad.bind("<KeyPress>",self.only_character_key)


        self.entry_soyad = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="Soyad",
            width=160,
            height=40,
            font=("Roboto", 14)
        )
        self.entry_soyad.grid(row=2, column=1, padx=(10, 20), pady=10)
        self.entry_soyad.bind("<KeyPress>",self.only_character_key)


        # 2. Satır: Yaş ve Telefon (Yan Yana)
        self.entry_yas = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="Yaş",
            width=160,
            height=40,
            font=("Roboto", 14)
        )
        self.entry_yas.grid(row=3, column=0, padx=(20, 10), pady=10)
        self.entry_yas.bind("<KeyPress>", self.only_number_key)


        self.entry_tel = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="Tel No (5XX...)",
            width=160,
            height=40,
            font=("Roboto", 14)
        )
        self.entry_tel.grid(row=3, column=1, padx=(10, 20), pady=10)
        self.entry_tel.bind("<KeyPress>", self.only_number_key)

        # 3. Satır: Email (Tam Genişlik)
        self.entry_email = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="E-Posta Adresi",
            height=40,
            font=("Roboto", 14)
        )
        self.entry_email.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
   
        # 4. Satır: Şifre (Tam Genişlik)
        self.entry_password = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="Şifre Belirle",
            height=40,
            show="*",
            font=("Roboto", 14)
        )
        self.entry_password.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Kayıt Ol Butonu
        self.btn_register = ctk.CTkButton(
            self.register_frame,
            text="KAYIT OL",
            fg_color="#1ABC9C",
            hover_color="#16A085",
            height=45,
            font=("Roboto", 15, "bold"),
            corner_radius=8,
            command=self.register_event
        )
        self.btn_register.grid(row=6, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

        # Giriş Yap Linki
        self.btn_login_link = ctk.CTkButton(
            self.register_frame,
            text="Zaten hesabın var mı? Giriş Yap",
            fg_color="transparent",
            text_color="#BDC3C7",
            hover_color="#34495E",
            font=("Roboto", 12),
            cursor="hand2",
            command=self.go_to_login
        )
        self.btn_login_link.grid(row=7, column=0, columnspan=2, padx=20, pady=(0, 30))

    def register_event(self):
        #Benzersiz değerleri ayırt etmemiz için data_manager'den tüm kullanıcıları çektik
        users=self.db.get_all_users()

        #Kullanıcıların id'lerini array olarak aldık
        existing_id=[user['id'] for user in users]
        id=self.get_unique_id(existing_id)
        if id is None:
            print("Benzersiz id bulunamadı.")
        
        #Inputlardan gelen değerler
        name=self.entry_ad.get()
        surname=self.entry_soyad.get()
        age=self.entry_yas.get()
        phone=self.entry_tel.get()
        mail=self.entry_email.get()
        password=self.entry_password.get()

        #Kontroller
        degerler=[name,surname,age,phone,mail,password]
        for deger in degerler:
            if not deger:
                messagebox.showerror("Hata","Eksik Kısımları Doldurun")
                return

        #Yaş Kontrolü
        if int(age) < 18:
            messagebox.showerror("Hata","Araç kiralamak için 18 yaşından büyük olmalısınız!")
            return

        #Şifre Kontrolü
        if len(password) < 6:
            messagebox.showerror("Hata","Şifreniz 6 Karakterden Fazla Olmalı")
            return

        #Mail format Kontrolü
        if '@' not in mail:
            messagebox.showerror("Hata","Mail adresi doğru formatta değil")
            return
        
        allowed_domains = ["@gmail.com", "@hotmail.com"]
        if not any(mail.endswith(domain) for domain in allowed_domains):
            messagebox.showerror("Hata", "Mail adresiniz yalnızca @gmail.com veya @hotmail.com olabilir!")
            return
        
        #Telefon numarası uzunluk kontrolü
        if len(phone) != 11:
            messagebox.showerror("Hata","Telefon numarası 11 karakterden oluşmalı!")
            return
        

        #Aynı mail ve telefon kontrolü
        for user in users:
            if user['phone'] == phone:
                messagebox.showerror("Hata","Bu telefon numarası sistemde kayıtlı!")
                return

        for user in users:
            if user['mail'] == mail:
                messagebox.showerror("Hata","Bu mail adresi sistemde kayıtlı")
                return
            
        #Verilerimiz kontrollerden geçerse data_manager dosyasındaki user_register fonksiyonu ile dosyaya yazıyoruz
        success=self.db.user_register(id,name,surname,password,age,mail,phone)

        if success:
            messagebox.showinfo("Başarılı","Kayıt Başarılı")
            from ui.loginPage import LoginPage
            self.destroy()
            LoginPage(self.master,self.controller,self.db).pack(expand=True,fill="both")
        else:
            messagebox.showerror("Hata","Kayıt esnasında bir hata oluştu!")

        
    def go_to_login(self):
        from ui.loginPage import LoginPage
        self.destroy()
        LoginPage(self.master,self.controller,self.db).pack(expand=True, fill="both")

    #ID Ataması İçin Kullanacağımız fonksiyon
    def get_unique_id(self, existing_ids):
        for i in range(101):
            if i not in existing_ids:
                return i
        return None
    
    def only_number_key(self,event):
            # Kontrol tuşlarına izin ver
        if event.keysym in ("BackSpace", "Tab", "Left", "Right", "Delete"):
            return

        # Rakam değilse engelle
        if not event.char.isdigit():
            return "break"
        
    def only_character_key(self,event):
        if event.keysym in ("BackSpace","Tab","Left","Right","Delete"):
            return
        
        if not event.char.isalpha():
            return "break"
