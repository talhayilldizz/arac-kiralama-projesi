import customtkinter as ctk
from PIL import Image
import os

class MusteriSayfasi(ctk.CTkFrame):
    def __init__(self, parent, controller,db_manager, current_user=None):
        super().__init__(parent, fg_color="#ECF0F1")
        self.controller = controller
        self.db = db_manager
        self.current_user = current_user

        self.grid_columnconfigure(1, weight=1) 
        self.grid_columnconfigure(0, minsize=300)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color="#2C3E50")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)

        self.lbl_baslik = ctk.CTkLabel(
            self.sidebar, 
            text="ARAÇ KİRALA", 
            font=("Roboto", 24, "bold"), 
            text_color="#FFFFFF"
        )
        self.lbl_baslik.grid(row=0, column=0, padx=20, pady=(35, 5))

        ctk.CTkLabel(
            self.sidebar, 
            text="FİLTRELE", 
            font=("Roboto", 12, "bold"), 
            text_color="#BDC3C7", 
            anchor="w"
        ).grid(row=1, column=0, padx=20, pady=(20, 20), sticky="w")


        KUTU_RENGI = "#34495E"     
        KENARLIK_RENGI = "#7F8C8D"  
        YAZI_RENGI = "#95A5A6"     
        
        self.combo_marka = ctk.CTkComboBox(
            self.sidebar, 
            values=["Tümü", "Fiat", "Renault", "BMW", "Mercedes", "Volvo", "Audi"], 
            height=35,
            font=("Roboto", 14),
            fg_color=KUTU_RENGI,      
            text_color=YAZI_RENGI,    
            button_color=KUTU_RENGI,
            border_width=0, 
            button_hover_color="#2C3E50",
            dropdown_fg_color=KUTU_RENGI,
            dropdown_text_color="white" 
        )
        self.combo_marka.set("Marka") 
        self.combo_marka.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")

     
        self.combo_model = ctk.CTkComboBox(
            self.sidebar, 
            values=["Tümü", "Egea", "Clio", "3.20i", "C200", "S90", "A6"], 
            height=35,
            font=("Roboto", 14),
            fg_color=KUTU_RENGI,         
            text_color=YAZI_RENGI,    
            button_color=KUTU_RENGI,
            border_width=0, 
            button_hover_color="#2C3E50",
            dropdown_fg_color=KUTU_RENGI,
            dropdown_text_color="white"
        )
        self.combo_model.set("Model") 
        self.combo_model.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.opt_fiyat = ctk.CTkComboBox(
            self.sidebar, 
            values=["Fark etmez", "0 - 1000 TL", "1000 - 3000 TL", "3000+ TL"], 
            height=35,
            font=("Roboto", 14),
            fg_color=KUTU_RENGI,
            text_color=YAZI_RENGI,    
            button_color=KUTU_RENGI,  
            border_width=0,
            button_hover_color="#2C3E50",
            dropdown_fg_color=KUTU_RENGI,
            dropdown_text_color="white"
        )
        self.opt_fiyat.set("Fiyat Aralığı") 
       
        self.opt_fiyat.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.btn_uygula = ctk.CTkButton(
            self.sidebar, 
            text="LİSTELE", 
            fg_color="#1ABC9C", 
            height=45, 
            font=("Roboto", 14, "bold"), 
            hover_color="#16A085"
        )
        self.btn_uygula.grid(row=5, column=0, padx=20, pady=30, sticky="ew")

        #SAĞ 
        
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.top_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.top_bar.pack(fill="x", pady=(10, 10))

        ctk.CTkLabel(
            self.top_bar, 
            text="ARAÇ LİSTESİ", 
            font=("Roboto", 20, "bold"), 
            text_color="#05113E"
        ).pack(side="left", pady=5)
        
        self.profil_menu = ctk.CTkOptionMenu(
            self.top_bar, 
            values=["Profilim", "Çıkış Yap"], 
            width=140, 
            fg_color="#2C3E50", 
            corner_radius=15,
            command=self.profile_git
        )
        self.profil_menu.set("👤 Hesabım")
        self.profil_menu.pack(side="right")

        self.main_scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True)
        
        musait_araclar = [
            {"ad": "Fiat Egea", "fiyat": "1000 ₺", "resim": "egea.png"},
            {"ad": "Renault Clio", "fiyat": "900 ₺", "resim": "clio.png"},
            {"ad": "Toyota Corolla", "fiyat": "1200 ₺", "resim": "corolla.png"},
            {"ad": "Honda Civic", "fiyat": "1300 ₺", "resim": "civic.png"},
            {"ad": "Ford Focus", "fiyat": "1250 ₺", "resim": "focus.png"},
        ]
        
        kirada_olanlar = [
            {"ad": "BMW 5.20i", "fiyat": "3500 ₺", "resim": "bmw.png"},
            {"ad": "Mercedes C200", "fiyat": "4000 ₺", "resim": "mercedes.png"},
            {"ad": "Volvo S90", "fiyat": "4500 ₺", "resim": "volvo.png"},
            {"ad": "Audi A6", "fiyat": "4200 ₺", "resim": "audi.png"},
        ]

        bakimda_olanlar = [
            {"ad": "VW Passat", "fiyat": "Bakımda", "resim": "passat.png"},
            {"ad": "Skoda Octavia", "fiyat": "Bakımda", "resim": "skoda.png"},
        ]

        self.bolum_olustur(baslik="MÜSAİT ARAÇLAR", renk="#27AE60", arac_listesi=musait_araclar)
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#BDC3C7").pack(fill="x", pady=15, padx=10)

        self.bolum_olustur(baslik="KİRADA OLANLAR", renk="#E67E22", arac_listesi=kirada_olanlar)
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#BDC3C7").pack(fill="x", pady=15, padx=10)

        self.bolum_olustur(baslik="BAKIMDA OLANLAR", renk="#C0392B", arac_listesi=bakimda_olanlar)


    def bolum_olustur(self, baslik, renk, arac_listesi):
        baslik_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        baslik_frame.pack(fill="x", pady=(5, 10))
        
        ctk.CTkFrame(baslik_frame, width=5, height=25, fg_color=renk).pack(side="left", padx=(10, 10))
        ctk.CTkLabel(baslik_frame, text=baslik, font=("Roboto", 16, "bold"), text_color="#2C3E50").pack(side="left")

        grid_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        grid_frame.pack(fill="both")

        for i in range(4):
            grid_frame.grid_columnconfigure(i, weight=1)

        for i, arac in enumerate(arac_listesi):
            row = i // 4
            col = i % 4
            self.kart_ekle(grid_frame, row, col, arac, renk)


    def kart_ekle(self, parent, r, c, arac_bilgisi, renk_tema):
        kutu = ctk.CTkFrame(parent, fg_color="white", corner_radius=8)
        kutu.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

        resim_adi = arac_bilgisi.get("resim", "yok.png")
        resim_yolu = os.path.join(os.path.dirname(__file__), "assets", resim_adi)

        try:
            img_data = Image.open(resim_yolu)
            resim_objesi = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(130, 75))
            ctk.CTkLabel(kutu, text="", image=resim_objesi).pack(pady=(5,0))
        except:
            
            ctk.CTkFrame(kutu, height=75, width=130, fg_color="#BDC3C7", corner_radius=6).pack(pady=(5,0))

        
        ctk.CTkLabel(kutu, text=arac_bilgisi["ad"], font=("Roboto", 12, "bold"), text_color="#2C3E50").pack(pady=(3,0))
        ctk.CTkLabel(kutu, text=arac_bilgisi["fiyat"], font=("Roboto", 12, "bold"), text_color=renk_tema).pack(pady=0)

        musait_mi = renk_tema.lower() == "#27ae60"
        btn_text = "KİRALA" if musait_mi else "DETAY"
        btn_state = "normal"  

        btn_color = "#2C3E50"

        ctk.CTkButton(
            kutu, 
            text=btn_text, 
            fg_color=btn_color, 
            height=22, 
            width=80, 
            state=btn_state,
            font=("Roboto", 10, "bold")
        ).pack(pady=(2, 8))

    def profile_git(self, secim):
        if secim == "Profilim":
            from ui.profilePage import ProfilSayfasi
            self.destroy()  # Mevcut sayfayı kapat

            # --- DÜZELTME BURADA ---
            # .pack() yerine .grid() kullanıyoruz
            app = ProfilSayfasi(self.master, self.controller, self.db, self.current_user)
            app.grid(row=0, column=0, sticky="nsew")

        elif secim == "Çıkış Yap":
            from ui.loginPage import LoginPage
            self.destroy()  # Mevcut sayfayı kapat

            # Burada da .grid() kullanalım ki tutarlı olsun
            app = LoginPage(self.master, self.controller, self.db)
            app.grid(row=0, column=0, sticky="nsew")

        # Menü yazısını resetle
        #self.profil_menu.set("👤 Hesabım")

 
