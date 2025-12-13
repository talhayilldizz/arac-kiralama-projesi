import customtkinter as ctk
from tkinter import messagebox
from ai.price_estimate import fiyat_tahmin_et


class TahminSayfasi(ctk.CTkFrame):
    def __init__(self, parent, controller, db_manager):
        super().__init__(parent, fg_color="#ECF0F1")
        self.controller = controller
        self.db = db_manager

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=120)
        self.grid_columnconfigure(0, weight=1)

       
        self.header_frame = ctk.CTkFrame(
            self,
            height=120,
            corner_radius=0,
            fg_color="#2C3E50"
        )
        self.header_frame.grid(row=0, column=0, sticky="nsew")
        self.header_frame.grid_columnconfigure(1, weight=1)

        #Geri Butonu
        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="←",
            width=40,
            height=40,
            font=("Roboto", 18, "bold"),
            fg_color="#34495E",
            hover_color="#3D566E",
            corner_radius=10,
            command=self.admin_page
        )
        self.back_button.grid(row=0, column=0, padx=20, pady=35, sticky="w")

        # Başlık
        self.label = ctk.CTkLabel(
            self.header_frame,
            text="Araç Fiyatı Tahmin Edin",
            font=("Roboto", 22, "bold"),
            text_color="#FFFFFF"
        )
        self.label.grid(row=0, column=1)

        
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew", pady=25)

        # Form
        form_frame = ctk.CTkFrame(
            content_frame,
            fg_color="#FFFFFF",
            corner_radius=20,
            border_width=1,
            border_color="#DADFE3"
        )
        form_frame.pack(pady=15, padx=40)

        entry_style = {
            "width": 300,
            "height": 38,
            "font": ("Roboto", 14),
            "fg_color": "#F7F9FA",
            "border_color": "#D0D3D4",
            "text_color": "#2C3E50"
        }

        self.entry_marka = ctk.CTkEntry(form_frame, placeholder_text="Marka", **entry_style)
        self.entry_marka.grid(row=0, column=0, padx=25, pady=(20, 8))

        self.entry_model = ctk.CTkEntry(form_frame, placeholder_text="Model", **entry_style)
        self.entry_model.grid(row=1, column=0, padx=25, pady=8)

        self.entry_km = ctk.CTkEntry(form_frame, placeholder_text="KM", **entry_style)
        self.entry_km.grid(row=2, column=0, padx=25, pady=8)

        self.entry_yil = ctk.CTkEntry(form_frame, placeholder_text="Model Yılı", **entry_style)
        self.entry_yil.grid(row=3, column=0, padx=25, pady=8)

        self.combo_hasar = ctk.CTkComboBox(
            form_frame,
            values=[
                "Hasarsız",
                "Lokal Boyalı",
                "Değişenli",
                "Ağır Hasarlı"
            ],
            state="readonly",
            width=300,
            height=38,
            font=("Roboto", 14),
            fg_color="#F7F9FA",
            border_color="#D0D3D4",
            text_color="#2C3E50",
            button_color="#BDC3C7",
            button_hover_color="#95A5A6"
        )
        self.combo_hasar.set("Hasarsız")
        self.combo_hasar.grid(row=4, column=0, padx=25, pady=(8, 20))

        # Buton
        ctk.CTkButton(
            content_frame,
            text="Fiyat Tahmin Et",
            font=("Roboto", 15, "bold"),
            fg_color="#2C3E50",
            hover_color="#34495E",
            width=260,
            height=48,
            corner_radius=12,
            command=self.tahmin_yap
        ).pack(pady=20)

        #Sonuc
        self.sonuc_frame = ctk.CTkFrame(
            content_frame,
            fg_color="#ECFDF5",
            corner_radius=15,
            border_width=1,
            border_color="#A7F3D0"
        )
        self.sonuc_frame.pack(pady=(10, 0), padx=40)

        self.sonuc_label = ctk.CTkLabel(
            self.sonuc_frame,
            text="",
            font=("Roboto", 18, "bold"),
            text_color="#047857"
        )
        self.sonuc_label.pack(padx=20, pady=15)

    # Tahmin
    def tahmin_yap(self):
        arac = {
            "marka": self.entry_marka.get(),
            "model": self.entry_model.get(),
            "km": self.entry_km.get(),
            "hasar_durumu": self.combo_hasar.get(),
            "model_yili": self.entry_yil.get()
        }

        fiyat = fiyat_tahmin_et(arac)

        self.sonuc_label.configure(
            text=f"Tahmini Günlük Fiyat: {fiyat} ₺"
        )

    def admin_page(self):
        from ui.adminPage import AdminSayfasi
        self.destroy()
        AdminSayfasi(self.master, self.controller,self.db).pack(expand=True, fill="both")
