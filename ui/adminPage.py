import customtkinter as ctk
from tkinter import messagebox
class AdminSayfasi(ctk.CTkFrame):
    def __init__(self,parent,controller, db_manager):
        super().__init__(parent,fg_color="#ECF0F1")
        self.controller=controller
        self.db = db_manager

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

        #Ücret
        self.entry_ucret=ctk.CTkEntry(
            self.form_frame,
            placeholder_text="Günlük Ücret"
        )
        self.entry_ucret.grid(row=5,column=0,padx=20,pady=8,sticky="ew")

        self.btn_add=ctk.CTkButton(
            self.form_frame,
            text="Araç Ekle",
            fg_color="#1ABC9C",
            height=40,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=8,
            command=self.btn_car_add
        )
        self.btn_add.grid(row=6, column=0, padx=20, pady=(30, 8), sticky="ew")

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
           
        self.btn_price.grid(row=7, column=0, padx=20, pady=(30, 8), sticky="ew")

        #Tablolar
        self.table_container=ctk.CTkFrame(self,fg_color="transparent")
        self.table_container.grid(row=0, column=1, padx=25, pady=25, sticky="nsew")

        #Araçlar Tablosu
        self.top_frame=ctk.CTkFrame(self.table_container, fg_color="transparent")
        self.top_frame.pack(side="top", fill="both", expand=True, pady=(0, 10))

        lbl_car_list=ctk.CTkLabel(
            self.top_frame,
            text="ARAÇLAR",
            font=("Roboto",20,"bold"),
            text_color="#05113E",
        )
        lbl_car_list.pack(anchor="w",pady=(0,5))


        #Araç Özelliklerinin Başlıklarının Olacağı Frame
        self.header_frame=ctk.CTkFrame(
            self.top_frame,
            fg_color="#34495E",
            height=40,
            corner_radius=5
        )
        self.header_frame.pack(fill="x", padx=0, pady=(0, 5))


        headers=["PLAKA", "MARKA", "MODEL", "ÜCRET", "DURUM", "İŞLEMLER"]
        for i in range(6):
            self.header_frame.grid_columnconfigure(i, weight=1)
            ctk.CTkLabel(self.header_frame, text=headers[i], text_color="white", font=("Segoe UI", 12, "bold")).grid(row=0, column=i, pady=10)

        self.car_list_frame=ctk.CTkScrollableFrame(
            self.top_frame,fg_color="transparent",
            height=200
        )
        self.car_list_frame.pack(fill="both",expand=True)

        #Kullanıcılar Tablosu

        self.bottom_frame=ctk.CTkFrame(
            self.table_container,
            fg_color="transparent"
        )
        self.bottom_frame.pack(side="bottom", fill="both", expand=True, pady=(10, 0))


        lbl_user_list=ctk.CTkLabel(
            self.bottom_frame,
            text="KULLANICILAR",
            font=("Roboto",20,"bold"),
            text_color="#2C3E50"
        )
        lbl_user_list.pack(anchor="w",pady=(0,5))

        #Kullanıcı Özelliklerinin Başlıklarının Olacağı Frame
        self.header_frame2 = ctk.CTkFrame(
            self.bottom_frame,
            fg_color="#34495E",
            height=40,
            corner_radius=5
        )
        self.header_frame2.pack(fill="x", padx=0, pady=(0, 5))

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
            self.bottom_frame,
            fg_color="transparent",
            height=200
        )
        self.user_list_frame.pack(fill="both", expand=True)

        self.get_all_users()


    def get_all_cars(self):
        print("Tüm Araçları Getirme Fonksiyonu")

    def btn_car_add(self):

        print("Araç Ekleme Fonksiyonu")

   
    def btn_car_edit(self):

        print("Araç Güncelleme Fonksiyonu")

    def btn_car_delete(self):

        print("Araç Silme Fonksiyonu")

    def btn_pricepage(self):
        from ui.pricePage import TahminSayfasi
        self.destroy()
        TahminSayfasi(self.master, self.controller,self.db).pack(expand=True, fill="both")


    #Her bir kullanıcı için bir satır
    def add_user_row(self, row, user):
        row_color = "#ECF0F1" if row % 2 == 0 else "transparent"
        
        row_frame = ctk.CTkFrame(
            self.user_list_frame, 
            fg_color=row_color, 
            corner_radius=6,
            height=45 # Buton sığsın diye yüksekliği biraz artırdım
        )
        row_frame.pack(fill="x", pady=2)

        values = [
            f"{user['name']} {user['surname']}",
            user["mail"],
            user["age"],
            user["phone"]
        ]

        # Sütun konfigürasyonu (Buton sütunu dahil)
        for i, width in enumerate(self.user_col_widths):
            row_frame.grid_columnconfigure(i, minsize=width, weight=1)

        # 1. ADIM: Yazıları Yerleştir (İlk 4 sütun)
        for i, value in enumerate(values):
            align_style = "ew" if i == 2 else "w" # Yaş ortalı
            padding_x = 0 if i == 2 else 10
            
            lbl = ctk.CTkLabel(
                row_frame,
                text=value,
                font=("Segoe UI", 12),
                text_color="#2C3E50",
                fg_color="transparent"
            )
            lbl.grid(row=0, column=i, sticky=align_style, padx=padding_x, pady=8)

        # 2. ADIM: Butonu Yerleştir (5. Sütun -> index 4)
        # Not: command kısmında lambda kullandık ki hangi kullanıcının tıklandığını bilsin.
        btn_history = ctk.CTkButton(
            row_frame,
            text="Kiraladığı Araçlar",
            font=("Segoe UI", 11, "bold"),
            height=28,
            width=120,
            fg_color="#3498DB",
            hover_color="#2980B9",
            text_color="white",
        )
        btn_history.grid(row=0, column=4, padx=10, pady=5)

    def get_all_users(self):
        for widget in self.user_list_frame.winfo_children():
            widget.destroy()

        users = self.db.get_all_users()

        for i, user in enumerate(users):
            self.add_user_row(i, user)