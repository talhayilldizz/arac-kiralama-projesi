import customtkinter as ctk
from PIL import Image
import os

class ProfilSayfasi(ctk.CTkFrame):
    def __init__(self, parent, controller,db_manager, current_user):
        super().__init__(parent, fg_color="#ECF0F1")
        self.controller = controller
        self.db_manager = db_manager
        self.current_user = current_user

        self.grid_columnconfigure(0, weight=0) 
        self.grid_columnconfigure(1, weight=1) 
        self.grid_rowconfigure(0, weight=1)

        
        self.sidebar = ctk.CTkFrame(self, width=400, corner_radius=0, fg_color="#2C3E50")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)
   
        self.lbl_baslik = ctk.CTkLabel(
            self.sidebar, 
            text="PROFİLİM", 
            font=("Roboto", 24, "bold"), 
            text_color="#FFFFFF"
        )
        self.lbl_baslik.grid(row=0, column=0, padx=20, pady=(35, 20), sticky="nsew")

        self.profil_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.profil_container.grid(row=1, column=0, padx=50, pady=(0, 15))

        self.foto_cerceve = ctk.CTkFrame(
            self.profil_container, 
            width=100, 
            height=100, 
            corner_radius=50,
            fg_color="#34495E"
            
        )
        self.foto_cerceve.pack(side="left")
        
        try:
            img_path = os.path.join(os.path.dirname(__file__), "assets", "profil.png")
            img_data = Image.open(img_path)
            profil_img = ctk.CTkImage(img_data, size=(70, 70)) 
            lbl_img = ctk.CTkLabel(self.foto_cerceve, text="", image=profil_img)
            lbl_img.place(relx=0.5, rely=0.5, anchor="center")
        except:
            ctk.CTkLabel(self.foto_cerceve, text="👤", font=("Roboto", 40), text_color="#BDC3C7").place(relx=0.5, rely=0.5, anchor="center")


        KUTU_RENGI = "#34495E"      
        YAZI_RENGI = "#BDC3C7"     
        
        kullanici_bilgileri = {
            "Ad": self.current_user.get("name", ""),
            "Soyad": self.current_user.get("surname", ""),
            "Yaş": self.current_user.get("age", ""),
            "Tel No": self.current_user.get("phone", ""),
            "Gmail": self.current_user.get("mail", ""),
            "Şifre": self.current_user.get("password", "")
        }

        row_count = 2
        for etiket, deger in kullanici_bilgileri.items():
            
            ctk.CTkLabel(
                self.sidebar, 
                text=etiket, 
                text_color=YAZI_RENGI,
                font=("Roboto", 14, "bold"), 
                anchor="w"
            ).grid(row=row_count, column=0, padx=20, pady=(0, 0), sticky="w") 
          
            
            entry = ctk.CTkEntry(
                self.sidebar,
                width=200,
                height=35,
                font=("Roboto", 14),
                fg_color=KUTU_RENGI,
                border_width=0,
                text_color="white"
            )
            entry.insert(0, deger) 
            entry.grid(row=row_count+1, column=0, padx=20, pady=(0, 8), sticky="ew")
            
            row_count += 2

        self.btn_guncelle = ctk.CTkButton(
            self.sidebar, 
            text="BİLGİLERİ GÜNCELLE", 
            fg_color="#1ABC9C", 
            width=300,
            height=45, 
            font=("Roboto", 14, "bold"), 
            hover_color="#16A085"
        )
        self.btn_guncelle.grid(row=row_count+1, column=0, padx=20, pady=20, sticky="ew")


        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.top_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.top_bar.pack(fill="x", pady=(10, 10))

        ctk.CTkLabel(
            self.top_bar, 
            text="KİRALAMA HAREKETLERİ", 
            font=("Roboto", 20, "bold"), 
            text_color="#05113E"
        ).pack(side="left", pady=5)
        
        self.btn_geri = ctk.CTkButton(
            self.top_bar, 
            text="Araç Kiralama Sayfasına Dön", 
            fg_color="#8D3030",
            width=150, 
            height=30
        )
        self.btn_geri.pack(side="right")

        self.main_scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True)

        
        aktif_kiralamalar = [
            {"ad": "Mercedes C200", "fiyat": "4000 ₺", "resim": "mercedes.png", "durum": "Teslim Tarihi: Yarın"},
        ]
        
        gecmis_kiralamalar = [
            {"ad": "Renault Clio", "fiyat": "900 ₺", "resim": "clio.png", "durum": "Kiralama Tamamlandı", "tarih": "23.02.2025 - 29.02.2025"},
            {"ad": "Fiat Egea", "fiyat": "1000 ₺", "resim": "egea.png", "durum": "Kiralama Tamamlandı", "tarih": "14.04.202 - 20.04.2025"},
            {"ad": "Renault Clio", "fiyat": "900 ₺", "resim": "clio.png", "durum": "Kiralama Tamamlandı", "tarih": "23.11.2025 - 24.11.2025"},
            {"ad": "Ford Focus", "fiyat": "1250 ₺", "resim": "focus.png", "durum": "Kiralama Tamamlandı", "tarih": "06.12.2025 - 28.12.2025"},
            
        ]
        encok_kiralananlar=[

            {"ad": "Renault Clio", "fiyat": "900 ₺", "resim": "clio.png", "durum":"2 kere kiralandı"},
        ]

        
        self.bolum_olustur(baslik="GÜNCEL OLARAK KİRALADIĞINIZ ARAÇLAR", renk="#0CA246", arac_listesi=aktif_kiralamalar, buton_text="İADE ET")
        
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#BDC3C7").pack(fill="x", pady=20, padx=10)

        self.bolum_olustur(baslik="GEÇMİŞ KİRALAMALARINIZ", renk="#C11F1F", arac_listesi=gecmis_kiralamalar, buton_text="TEKRAR KİRALA")

        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#BDC3C7").pack(fill="x", pady=20, padx=10)
        
        self.bolum_olustur(baslik="EN ÇOK KİRALADIĞINIZ ARAÇLAR", renk="#F6D75C",arac_listesi=encok_kiralananlar, buton_text="TEKRAR KİRALA")


    def bolum_olustur(self, baslik, renk, arac_listesi, buton_text="DETAY"):
        baslik_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        baslik_frame.pack(fill="x", pady=(5, 10))
        
        ctk.CTkFrame(baslik_frame, width=5, height=25, fg_color=renk).pack(side="left", padx=(10, 10))
        ctk.CTkLabel(baslik_frame, text=baslik, font=("Roboto", 16, "bold"), text_color="#2C3E50").pack(side="left")

        grid_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        grid_frame.pack(fill="both")

        for i in range(4):
            grid_frame.grid_columnconfigure(i, weight=1)

        if not arac_listesi:
            ctk.CTkLabel(grid_frame, text="Kayıt bulunamadı.", text_color="gray").pack(pady=10)
        
        for i, arac in enumerate(arac_listesi):
            row = i // 4
            col = i % 4
            self.kart_ekle(grid_frame, row, col, arac, renk, buton_text)


    def kart_ekle(self, parent, r, c, arac_bilgisi, renk_tema, buton_text):
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
        
        durum_yazisi = arac_bilgisi.get("durum", arac_bilgisi["fiyat"])
        ctk.CTkLabel(kutu, text=durum_yazisi, font=("Roboto", 11), text_color="gray").pack(pady=0)
        
        if "tarih" in arac_bilgisi:
            ctk.CTkLabel(
                kutu, 
                text=arac_bilgisi["tarih"], 
                font=("Roboto", 10), 
                text_color="#0D0D0E" 
            ).pack(pady=(0, 0))
       
        ctk.CTkButton(
            kutu, 
            text=buton_text, 
            fg_color="#2C3E50", 
            height=22, 
            width=90, 
            font=("Roboto", 10, "bold")
        ).pack(pady=(5, 8))


if __name__ == "__main__":
    ctk.set_appearance_mode("Light")
    app = ctk.CTk()
    app.geometry("1200x800")
    app.title("Profil Sayfası ")
    sayfa = ProfilSayfasi(parent=app, controller=None)
    sayfa.pack(fill="both", expand=True)
    app.mainloop()