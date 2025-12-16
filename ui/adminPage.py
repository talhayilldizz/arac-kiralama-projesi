import customtkinter as ctk
from tkinter import messagebox
import re
from tkcalendar import DateEntry
from datetime import datetime

class AdminSayfasi(ctk.CTkFrame):
    def __init__(self,parent,controller, db_manager):
        super().__init__(parent,fg_color="#ECF0F1")
        self.controller=controller
        self.db = db_manager

        #Güncelleme işleminde kullanılacak
        self.edit_mode=False
        self.edit_car_plate=None

        #Aracı kiralayan kişinin idsi
        self.current_user_mail=None

        #Sayfayı 2 ye böldüm
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(0, minsize=300)
        self.grid_rowconfigure(0,weight=1)
        
        #Form Alanı
        self.form_frame=ctk.CTkFrame(self,width=300,corner_radius=0,fg_color="#2C3E50")
        self.form_frame.grid(row=0,column=0,sticky="nsew")
        self.form_frame.grid_rowconfigure(10, weight=1)

        #Sayfa Adı
        self.admin_label=ctk.CTkLabel(
            self.form_frame,
            text="Yönetici Sayfası",
            font=("Roboto",22,"bold"),
            text_color="#FFFFFF"
        )
        self.admin_label.grid(row=0, column=0, padx=20, pady=(30,10))

        lbl_form=ctk.CTkLabel(
            self.form_frame,
            text="Araç Ekleme Formu",
            font=("Roboto",14,"bold"),
            text_color="#BDC3C7"
        )
        lbl_form.grid(row=1,column=0,padx=20,pady=(0,20),sticky="w")

        #Form Kutuları
        #Plaka
        self.entry_plaka=ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Plaka"
        )
        self.entry_plaka.grid(row=2,column=0,padx=20,pady=8,sticky="ew")
        self.entry_plaka.bind("<KeyRelease>", self.plaka_format)

        #Marka
        self.entry_marka=ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Marka"
        )
        self.entry_marka.grid(row=3,column=0,padx=20,pady=8,sticky="ew")

        #Model
        self.entry_model=ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Model"
        )
        self.entry_model.grid(row=4,column=0,padx=20,pady=8,sticky="ew")
        
        #Yıl
        self.entry_yıl=ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Yıl"
        )
        self.entry_yıl.grid(row=5,column=0,padx=20,pady=8,sticky="ew")
        self.entry_yıl.bind("<KeyPress>", self.only_number_key)

        #Ücret
        self.entry_ucret=ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Günlük Ücret"
        )
        self.entry_ucret.grid(row=6,column=0,padx=20,pady=8,sticky="ew")
        self.entry_ucret.bind("<KeyPress>", self.only_number_key)

        #Ekle Butonu
        self.btn_add=ctk.CTkButton(
            self.form_frame,
            text="Araç Ekle",
            fg_color="#1ABC9C",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8,
            command=self.btn_car_add
        )
        self.btn_add.grid(row=7, column=0, padx=20, pady=(30, 8), sticky="ew")

        #Aİ butonu
        self.btn_price=ctk.CTkButton(
            self.form_frame,
            text="Fiyat Tahmin Et",
            fg_color="orange",
            text_color="#2C3E50",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8,
            command=self.btn_pricepage
        )
        self.btn_price.grid(row=8, column=0, padx=20, pady=(30, 8), sticky="ew")

        #çıkış yap
        self.btn_cikis = ctk.CTkButton(
            self.form_frame,
            text="Çıkış Yap",
            fg_color="#C0392B",  # Kırmızı tonu
            hover_color="#E74C3C",  # Üzerine gelince açılan renk
            height=40,
            corner_radius=8,
            font=("Roboto", 14, "bold"),
            command=self.cikis_yap  # Tıklanınca çalışacak fonksiyon
        )
        # Row sayısını yüksek veriyoruz ki en altta kalsın
        self.btn_cikis.grid(row=11, column=0, padx=20, pady=(30,8), sticky="ew")


        #Tablolar
        self.table_container=ctk.CTkFrame(self,fg_color="transparent")
        self.table_container.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")
        self.table_container.grid_rowconfigure(1,weight=1) # bottom_frame'in esnemesini sağlar
        self.table_container.grid_columnconfigure(0, weight=1)

        #Araçlar Tablosu
        self.top_frame=ctk.CTkFrame(self.table_container, fg_color="transparent")
        self.top_frame.grid(row=0,column=0,sticky="nsew",pady=(0,10))

        lbl_car_list=ctk.CTkLabel(
            self.top_frame,
            text="ARAÇLAR",
            font=("Roboto",20,"bold"),
            text_color="#05113E",
        )
        lbl_car_list.pack(anchor="w",pady=(0,5))

        #Araç Özelliklerinin Başlıklarının Olacağı Frame
        self.header_frame = ctk.CTkFrame(
            self.top_frame,
            fg_color="#34495E",
            height=40,
            corner_radius=5
        )
        self.header_frame.pack(fill="x", padx=0, pady=(0, 5))


        self.car_col_widths = [90, 100, 100, 60, 90, 80, 150] 
        headers = ["PLAKA", "MARKA", "MODEL", "YIL", "ÜCRET", "DURUM", "İŞLEM"]
        
        for i, header in enumerate(headers):
            self.header_frame.grid_columnconfigure(i, weight=1, minsize=self.car_col_widths[i])
            ctk.CTkLabel(
                self.header_frame, 
                text=header, 
                text_color="white", 
                font=("Segoe UI", 12, "bold")
            ).grid(row=0, column=i, pady=10, sticky="ew")

        self.car_list_frame=ctk.CTkScrollableFrame(
            self.top_frame,fg_color="transparent",
            height=200
        )
        self.car_list_frame.pack(fill="both",expand=True)

        # Kullanıcılar ve Kiralanan araçlar
        self.bottom_frame=ctk.CTkFrame(
            self.table_container,
            fg_color="transparent"
        )
        self.bottom_frame.grid(row=1,column=0,sticky="nsew",pady=(10,0))

        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)
        self.bottom_frame.grid_rowconfigure(0, weight=1)

        # Kullanıcı Listesi Alanı 
        self.user_list_area = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.user_list_area.grid(row=0, column=0, sticky="nsew")
        self.user_list_area.configure(width=0)
        self.user_list_area.grid_rowconfigure(2, weight=1)
        self.user_list_area.grid_columnconfigure(0, weight=1)

        lbl_user_list=ctk.CTkLabel(
            self.user_list_area,
            text="KULLANICILAR",
            font=("Roboto",20,"bold"),
            text_color="#2C3E50"
        )
        lbl_user_list.grid(row=0, column=0, sticky="w",padx=20, pady=(0,5))

        #Kullanıcı Özelliklerinin Başlıklarının Olacağı Frame
        self.header_frame2 = ctk.CTkFrame(
            self.user_list_area, # user_list_area içinde
            fg_color="#34495E",
            height=40,
            corner_radius=5,
            # width=100
        )
        self.header_frame2.grid(row=1, column=0, sticky="ew",padx=20, pady=(0, 5))

        # Sütun genişliklerini sabitliyoruz ki aşağıda da aynısını kullanalım
        self.user_col_widths = [170, 200, 60, 130, 160] 
        headers = ["AD SOYAD", "MAIL", "YAŞ", "TELEFON","GEÇMİŞ"]

        for i, header in enumerate(headers):
            self.header_frame2.grid_columnconfigure(i, minsize=self.user_col_widths[i], weight=1)
            align = "ew" if i in [2, 4] else "w"

            ctk.CTkLabel(
                self.header_frame2,
                text=header,
                text_color="white",
                font=("Segoe UI", 12, "bold")
            ).grid(row=0, column=i, padx=10, pady=10, sticky=align)

        self.user_list_frame = ctk.CTkScrollableFrame(
            self.user_list_area, # user_list_area içinde
            fg_color="transparent"
        )
        self.user_list_frame.grid(row=2, column=0, sticky="nsew") # Kullanıcı listesi dikeyde esner


        # Kiralanan araçlar listesi (bottom_frame Sütun 1)
        self.rented_car_area = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.rented_car_area.grid(row=0, column=1, sticky="nsew")
        self.rented_car_area.configure(width=0)

        self.rented_car_area.grid_rowconfigure(2, weight=1)
        self.rented_car_area.grid_columnconfigure(0, weight=1)

        self.lbl_rented_list = ctk.CTkLabel(
            self.rented_car_area,
            text="KİRALAMA GEÇMİŞİ",
            font=("Roboto", 16, "bold"),
            text_color="#2C3E50",
            anchor="w"
        )
        self.lbl_rented_list.grid(row=0,column=0,sticky="ew",padx=20,pady=(0,5)) 

        self.rented_header_frame = ctk.CTkFrame(
            self.rented_car_area,
            fg_color="#34495E",
            height=40,
            corner_radius=5
        )
        self.rented_header_frame.grid(row=1, column=0, sticky="ew", pady=(0, 5))

        self.rented_col_widths = [80, 80, 80, 80,80]
        rented_headers = ["PLAKA", "MARKA", "BAŞ.", "BİT.","ÜCRET"]

        for i, header in enumerate(rented_headers):
            self.rented_header_frame.grid_columnconfigure(i, weight=1, minsize=self.rented_col_widths[i])
            ctk.CTkLabel(
                self.rented_header_frame, 
                text=header, 
                text_color="white", 
                font=("Segoe UI", 11, "bold")
            ).grid(row=0, column=i, pady=10, sticky="ew")

        self.rented_list_frame = ctk.CTkScrollableFrame(
            self.rented_car_area,
            fg_color="transparent"
        )
        self.rented_list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10)) 

        self.get_all_cars()
        self.get_all_users()



    def btn_car_add(self):
        plate=self.entry_plaka.get()
        brand=self.entry_marka.get().capitalize()
        model=self.entry_model.get().capitalize()
        year=self.entry_yıl.get()
        price=self.entry_ucret.get()

        degerler=[plate,brand,model,year,price]
        for deger in degerler:
            if not deger:
                messagebox.showerror("Hata","Eksik Kutuları Doldurun!")
                return

        cars=self.db.get_all_cars()
        for car in cars:
            if car['plate'] == plate:
                messagebox.showerror("Hata","Bu plaka sistemde kayıtlı!")
                return
        
        success=self.db.add_car(brand,model,year,plate,price)

        if success:
            messagebox.showinfo("Başarılı","Araç Eklendi")
            self.get_all_cars()

            self.entry_plaka.delete(0,"end")
            self.entry_marka.delete(0,"end")
            self.entry_model.delete(0,"end")
            self.entry_yıl.delete(0,"end")
            self.entry_ucret.delete(0,"end")
        else:
            messagebox.showwarning("Hata","Araç Eklenemedi")
        

        
    def only_number_key(self,event):
            # Kontrol tuşlarına izin ver
        if event.keysym in ("BackSpace", "Tab", "Left", "Right", "Delete"):
            return

        # Rakam değilse engelle
        if not event.char.isdigit():
            return "break"

   
    def btn_car_edit(self,car_plate):
        car=self.db.get_car_by_id(car_plate)

        #İnputları temizleyip güncellenecek aracın bilgilerini yazmamız lazım
        if not car:
            messagebox.showerror("Hata","Araç Bulunamadı..")
            return
        
        #plaka
        self.entry_plaka.delete(0,"end")
        self.entry_plaka.insert(0,car["plate"])

        #marka
        self.entry_marka.delete(0,"end")
        self.entry_marka.insert(0,car["brand"])

        #model
        self.entry_model.delete(0,"end")
        self.entry_model.insert(0,car["model"])

        #yıl
        self.entry_yıl.delete(0,"end")
        self.entry_yıl.insert(0,car["year"])

        #ücret
        self.entry_ucret.delete(0,"end")
        self.entry_ucret.insert(0,car["price"])

        self.edit_mode=True
        self.edit_car_plate=car_plate

        self.btn_add.configure(text="Güncelle",fg_color="blue",command=self.save_update_car)


    def save_update_car(self):
        new_plate=self.entry_plaka.get()
        brand=self.entry_marka.get().capitalize()
        model=self.entry_model.get().capitalize()
        year=self.entry_yıl.get()
        price=self.entry_ucret.get()

        degerler=[new_plate,brand,model,year,price]
        for deger in degerler:
            if not deger:
                messagebox.showerror("Hata","Eksik Kısımları Doldurun..")
                return
        
        cars=self.db.get_all_cars()
        for car in cars:
            if car['plate'] == new_plate and car['plate'] != self.edit_car_plate:
                messagebox.showerror("Hata","Bu plaka başka araca ait. Başka plaka deneyin.")
                return
        
        success=self.db.update_car(self.edit_car_plate,new_plate,brand,model,year,price)

        if success:
            messagebox.showinfo("Başarılı","Araç Güncellendi")
             #Inputlar Temizlenir
            self.entry_plaka.delete(0, 'end')
            self.entry_marka.delete(0, 'end')
            self.entry_model.delete(0, 'end')
            self.entry_yıl.delete(0, 'end')
            self.entry_ucret.delete(0, 'end')

            self.btn_add.configure(text="Araç Ekle", fg_color="#1ABC9C", command=self.btn_car_add)
            self.edit_mode=False
            self.edit_car_plate=None

            self.get_all_cars()
        else:
            messagebox.showerror("Hata","Bi sıkıntı oluştu. Araç Güncellenemdi.")
        
    

    def delete_car(self,car_plate):
        if messagebox.askyesno("Onay","Aracı Silmek İstediğinize Eminmisiniz?"):
            success=self.db.car_delete(car_plate)
            if success:
                messagebox.showinfo("Başarılı","Araç Silindi")
                self.get_all_cars()
            else:
                messagebox.showerror("Hata","Araç Kirada Olduğundan Silinemiyor!")


    def btn_pricepage(self):
        from ui.pricePage import TahminSayfasi
        self.destroy()
        TahminSayfasi(self.master, self.controller,self.db).pack(expand=True, fill="both")

    #Her araç için bir satır
    def add_car_row(self, row, car):
        row_color = "#ECF0F1" if row % 2 == 0 else "transparent"
        
        row_frame = ctk.CTkFrame(
            self.car_list_frame, 
            fg_color=row_color, 
            corner_radius=6,
            height=45
        )
        row_frame.pack(fill="x", pady=2)
        

        values = [
            car["plate"],
            car["brand"],
            car["model"],
            car["year"],
            f"{car['price']} TL",
            car["status"]
        ]
        
        # Sütun yapılandırmasını başlıklarla (car_col_widths) aynı yapıyoruz
        for i, width in enumerate(self.car_col_widths):
            row_frame.grid_columnconfigure(i, weight=1, minsize=width)

        # Verileri yerleştir (İlk 6 sütun)
        for i, value in enumerate(values):
            lbl = ctk.CTkLabel(
                row_frame,
                text=value,
                font=("Segoe UI", 12),
                text_color="#2C3E50",
                fg_color="transparent"
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=5, pady=8)

        actions_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=6, sticky="ew", padx=5, pady=5)
        
        # Butonları ortalamak için grid ayarı
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)

        btn_delete = ctk.CTkButton(
            actions_frame,
            text="Sil",
            font=("Segoe UI", 11, "bold"),
            height=28,
            width=60,
            fg_color="#C0392B",
            hover_color="#E74C3C",
            text_color="white",
            command=lambda c=car['plate']:(
                self.delete_car(c)
            )
        )
        btn_delete.grid(row=0, column=0, padx=2)

        btn_update = ctk.CTkButton(
            actions_frame,
            text="Guncelle",
            font=("Segoe UI", 11, "bold"),
            height=28,
            width=60,
            fg_color="#FF8E04",
            hover_color="#FF9100",
            text_color="white",
            command=lambda c=car["plate"]:(
                self.btn_car_edit(c)
            )
        )
        btn_update.grid(row=0, column=1, padx=2)



    #Her bir kullanıcı için bir satır
    def add_user_row(self, row, user):
        row_color = "#ECF0F1" if row % 2 == 0 else "transparent"
        
        row_frame = ctk.CTkFrame(
            self.user_list_frame, 
            fg_color=row_color, 
            corner_radius=6,
            height=45 
        )
        row_frame.pack(fill="x", pady=2)

        values = [
            f"{user['name']} {user['surname']}",
            user["mail"],
            user["age"],
            user["phone"]
        ]

        for i, width in enumerate(self.user_col_widths):
            row_frame.grid_columnconfigure(i, minsize=width, weight=1)

       
        for i, value in enumerate(values):
            align_style = "ew" if i == 2 else "w" 
            padding_x = 0 if i == 2 else 10
            
            lbl = ctk.CTkLabel(
                row_frame,
                text=value,
                font=("Segoe UI", 12),
                text_color="#2C3E50",
                fg_color="transparent"
            )
            lbl.grid(row=0, column=i, sticky=align_style, padx=padding_x, pady=8)

        btn_history = ctk.CTkButton(
            row_frame,
            text="Kiraladığı Araçlar",
            font=("Segoe UI", 11, "bold"),
            height=28,
            width=120,
            fg_color="#3498DB",
            hover_color="#2980B9",
            text_color="white",
            command=lambda mail=user['mail']:( 
                self.get_users_car(mail)
            )
        )
        btn_history.grid(row=0, column=4, padx=10, pady=5)


    #Tüm kullanıcıları getir
    def get_all_users(self):
        for widget in self.user_list_frame.winfo_children():
            widget.destroy()

        users = self.db.get_all_users()

        for i, user in enumerate(users):
            self.add_user_row(i, user)


    #Tüm araçları getir
    def get_all_cars(self):
            for widget in self.car_list_frame.winfo_children():
                widget.destroy()

            cars = self.db.get_all_cars()

            for i, car in enumerate(cars):
                self.add_car_row(i, car)


    #Plaka format
    def plaka_format(self, event=None):
        text = self.entry_plaka.get().upper() 
        text = re.sub(r'[^A-Z0-9 ]', '', text)  

        text = text.replace(" ", "")  
        if len(text) > 2:
            text = text[:2] + " " + text[2:]
        if len(text) > 6:
            text = text[:6] + " " + text[6:]

        self.entry_plaka.delete(0, "end")
        self.entry_plaka.insert(0, text)

        
        if len(text) > 10:
            self.entry_plaka.delete(9, "end")

    def cikis_yap(self):
        from ui.loginPage import LoginPage
        self.destroy()

        app = LoginPage(self.master, self.controller, self.db)
        app.grid(row=0, column=0, sticky="nsew")

    #Kullanıcının kiraladğı araçlar
    def get_users_car(self, user_mail):
        self.current_user_mail=user_mail
        
        for widget in self.rented_list_frame.winfo_children():
            widget.destroy()

        rentals = self.db.get_car_by_mail(user_mail) 

        if not rentals or not isinstance(rentals, list): 
            ctk.CTkLabel(
                self.rented_list_frame,
                text=f"'{user_mail}' kullanıcısının kiralama geçmişi bulunmamaktadır.",
                text_color="#C0392B",
                font=("Segoe UI", 12, "italic")
            ).pack(pady=20, padx=10)
            return
        
        for i, rental in enumerate(rentals):
             if not isinstance(rental, dict):
                 continue
                 
             self.add_rented_car_row(i, rental)

    def add_rented_car_row(self, row, rental):
        row_color = "#ECF0F1" if row % 2 == 0 else "transparent"
        row_frame = ctk.CTkFrame(self.rented_list_frame, fg_color=row_color, corner_radius=4, height=35)
        row_frame.pack(fill="x", pady=1)

        #ücret hesaplaması
        start_date = datetime.strptime(rental["start_date"], "%d.%m.%Y")
        finish_date = datetime.strptime(rental["finsh_date"], "%d.%m.%Y")

        gun_sayisi = (finish_date - start_date).days
        gun_sayisi = max(gun_sayisi, 1)
        toplam_tutar = gun_sayisi * int(rental["price"])


        # Görüntülenecek veriler (PLAKA, MARKA, BAŞ. Tarihi, BİT. Tarihi, TOPLAM ÜCR.)
        values = [
            rental["plate"],
            rental["brand"],
            rental["start_date"],
            rental["finsh_date"],
            f"{toplam_tutar} TL"
        ]
        
        for i, width in enumerate(self.rented_col_widths):
            row_frame.grid_columnconfigure(i, weight=1, minsize=width)

        # Verileri yerleştir
        for i, value in enumerate(values):
            lbl = ctk.CTkLabel(
                row_frame,
                text=value,
                font=("Segoe UI", 11),
                text_color="#2C3E50",
                fg_color="transparent"
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=3, pady=6)


    