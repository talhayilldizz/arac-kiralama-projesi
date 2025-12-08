import customtkinter as ctk

from tkinter import messagebox



class AdminSayfasi(ctk.CTkFrame):

    def __init__(self,parent,controller):

        super().__init__(parent,fg_color="#ECF0F1")

        self.controoler=controller


        #Sayfayı 2 ye böldüm

        self.grid_columnconfigure(1,weight=1)

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

        self.entry_plaka=ctk.CTkEntry(

            self.form_frame,

            placeholder_text="Marka"

        )

        self.entry_plaka.grid(row=3,column=0,padx=20,pady=8,sticky="ew")



        #Model

        self.entry_plaka=ctk.CTkEntry(

            self.form_frame,

            placeholder_text="Model"

        )

        self.entry_plaka.grid(row=4,column=0,padx=20,pady=8,sticky="ew")



        #Ücret

        self.entry_plaka=ctk.CTkEntry(

            self.form_frame,

            placeholder_text="Günlük Ücret"

        )

        self.entry_plaka.grid(row=5,column=0,padx=20,pady=8,sticky="ew")



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

            text_color="#2C3E50"

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

        self.header_frame2=ctk.CTkFrame(

            self.bottom_frame,

            fg_color="#34495E",

            height=40,

            corner_radius=5

        )

        self.header_frame2.pack(fill="x", padx=0, pady=(0, 5))



        headers=["ID", "AD", "MAIL","KIRALANAN ARACLAR"]

        for i in range(4):

            self.header_frame2.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(self.header_frame2, text=headers[i], text_color="white", font=("Segoe UI", 12, "bold")).grid(row=0, column=i, pady=10)



        self.user_list_frame=ctk.CTkScrollableFrame(

            self.bottom_frame,

            fg_color="transparent",

            height=200

        )

        self.user_list_frame.pack(fill="both",expand=True)



    def get_all_cars(self):

        print("Tüm Araçları Getirme Fonksiyonu")



    def get_all_users(self):

        print("Tüm Kullanıcıları Getirme Fonksiyonu")



    def btn_car_add(self):

        print("Araç Ekleme Fonksiyonu")

   



    def btn_car_edit(self):

        print("Araç Güncelleme Fonksiyonu")



    def btn_car_delete(self):

        print("Araç Silme Fonksiyonu")