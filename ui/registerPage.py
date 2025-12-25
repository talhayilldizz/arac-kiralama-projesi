import customtkinter as ctk
from tkinter import messagebox


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller, db_manager):
        super().__init__(parent, fg_color="#ECF0F1")
        self.__controller = controller
        self.__db=db_manager

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

       
        self.register_frame.grid_columnconfigure((0, 1), weight=1)

        
        self.lbl_title=ctk.CTkLabel(
            self.register_frame,
            text="HESAP OLUŞTUR",
            font=("Roboto", 24, "bold"),
            text_color="#FFFFFF"
        )
        self.lbl_title.grid(row=0, column=0, columnspan=2, padx=20, pady=(30, 5))

        
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
            placeholder_text="Tel No (05XX...)",
            width=160,
            height=40,
            font=("Roboto", 14)
        )
        self.entry_tel.grid(row=3, column=1, padx=(10, 20), pady=10)
        self.entry_tel.bind("<KeyPress>", self.only_number_key)


        self.entry_email = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="E-Posta Adresi",
            height=40,
            font=("Roboto", 14)
        )
        self.entry_email.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
   
        self.entry_password = ctk.CTkEntry(
            self.register_frame,
            placeholder_text="Şifre Belirle",
            height=40,
            show="*",
            font=("Roboto", 14)
        )
        self.entry_password.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

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
        users=self.__db.get_all_users()


        #sistemde kayıtlı kullanıcıların id dizisi
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

        if mail.startswith('@'):
            messagebox.showerror("Hata", "Mail adresinin başına kullanıcı adı yazmalısınız!")
            return

        if ' ' in mail:
            messagebox.showerror("Hata", "Mail adresinde boşluk olamaz!")
            return

       
        if ".." in mail:
            messagebox.showerror("Hata", "Mail adresinde yan yana iki nokta (..) bulunamaz.")
            return

       
        yasakli_karakterler = ["\\","ş", "ü", "ö", "ç", "ğ", "ı", "Ş", "Ü", "Ö", "Ç", "Ğ", "İ", "(", ")", "*", "/"]
        for harf in mail:
            if harf in yasakli_karakterler:
                messagebox.showerror("Hata", "Mail adresinde Türkçe karakter veya özel sembol kullanmayınız.")
                return

        # @ işaretinden önceki kısmı alalım
        kullanici_adi = mail.split('@')[0]
        mail_form =mail.split('@')[-1]

        correct_mail_forms = ['gmail.com', 'hotmail.com', 'outlook.com']

        if mail_form not in correct_mail_forms:
            messagebox.showerror("Hata", "Mail adresi formu hatalı, lütfen geçerli bir form girin. ")
            return

        # Kullanıcı adı en az 3 karakter olsun
        if len(kullanici_adi) < 3:
            messagebox.showerror("Hata", "Mail adresi çok kısa, lütfen geçerli bir adres girin.")
            return

        # Maili @ işaretinden ikiye bölüyoruz
        parts = mail.split('@')

        # Eğer split sonucu hatalıysa
        if len(parts) < 2:
            return

        username = parts[0]  # @'den önceki kısım

        if not username[0].isalpha():
            messagebox.showerror("Hata","Mail adresi mutlaka bir harf ile başlamalıdır! (Rakam veya sembolle başlayamaz)")
            return

        if not username[-1].isalnum():
            messagebox.showerror("Hata","Mail kullanıcı adı nokta veya özel karakterle bitemez! (@ işaretinden önce harf veya rakam olmalı)")
            return

        allowed_domains = ["@gmail.com", "@hotmail.com"]
        if not any(mail.endswith(domain) for domain in allowed_domains):
            messagebox.showerror("Hata", "Mail adresiniz yalnızca @gmail.com veya @hotmail.com olabilir!")
            return

        import re
        tel_pattern = r'^05[0-9]{9}$'

        if not re.match(tel_pattern, phone):
            messagebox.showwarning("Geçersiz Telefon",
                                   "Telefon numarası '05' ile başlamalı ve toplam 11 haneli olmalıdır.\nÖrn: 05551234567")
            return


        # regex yöntemi
        import re
        kural = r"^[a-z0-9._-]+@[a-z0-9.-]+\.[a-z]{2,}$"
        if not re.match(kural, mail):
            messagebox.showerror("Hata", "hatalı mail!")
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

        success=self.__db.user_register(id,name,surname,password,age,mail,phone)

        if success:
            messagebox.showinfo("Başarılı","Kayıt Başarılı")
            from ui.loginPage import LoginPage
            self.destroy()
            LoginPage(self.master,self.__controller,self.__db).pack(expand=True,fill="both")
        else:
            messagebox.showerror("Hata","Kayıt esnasında bir hata oluştu!")

        
    def go_to_login(self):
        from ui.loginPage import LoginPage
        self.destroy()
        LoginPage(self.master,self.__controller,self.__db).pack(expand=True, fill="both")

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
