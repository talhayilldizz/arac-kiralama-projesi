import customtkinter as ctk
from PIL import Image
import os
import json
from tkinter import messagebox
from datetime import datetime

class ProfilSayfasi(ctk.CTkFrame):
    def __init__(self, parent, controller,db_manager, current_user):
        super().__init__(parent, fg_color="#ECF0F1")
        self.controller = controller
        self.db_manager = db_manager
        self.current_user = current_user

        self.entry_widgets = {}

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
            base_path = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(base_path, "..", "assets", "profil.png")
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

            self.entry_widgets[etiket] = entry
            
            row_count += 2

        self.btn_guncelle = ctk.CTkButton(
            self.sidebar, 
            text="BİLGİLERİ GÜNCELLE", 
            fg_color="#1ABC9C", 
            width=300,
            height=45, 
            font=("Roboto", 14, "bold"), 
            hover_color="#16A085",
            command=self.bilgileri_guncelle
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
            height=30,
            command=self.musteri_sayfasina_git
        )
        self.btn_geri.pack(side="right")

        self.main_scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True)

        self.aktif_kiralamalar = []
        self.gecmis_kiralamalar = []
        
        self.verileri_yukle() 
        self.listeleri_ciz()
               
      
    def listeleri_ciz(self):
         
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        self.bolum_olustur(baslik="GÜNCEL OLARAK KİRALADIĞINIZ ARAÇLAR", renk="#0CA246", arac_listesi=self.aktif_kiralamalar, buton_text="İADE ET")
        
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#BDC3C7").pack(fill="x", pady=20, padx=10)

        self.bolum_olustur(baslik="GEÇMİŞ KİRALAMALARINIZ", renk="#C11F1F", arac_listesi=self.gecmis_kiralamalar, buton_text="TEKRAR KİRALA")   
      


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
        base_path = os.path.dirname(os.path.abspath(__file__))
        resim_yolu = os.path.join(base_path, "..", "assets", resim_adi)
        
        try:
            img_data = Image.open(resim_yolu)
            resim_objesi = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(130, 75))
            ctk.CTkLabel(kutu, text="", image=resim_objesi).pack(pady=(5,0))
        except:
            ctk.CTkFrame(kutu, height=75, width=130, fg_color="#BDC3C7", corner_radius=6).pack(pady=(5,0))

        ctk.CTkLabel(kutu, text=arac_bilgisi["marka"] + " " + arac_bilgisi["model"], font=("Roboto", 12, "bold"), text_color="#2C3E50").pack(pady=(3,0))
        
        durum_yazisi = arac_bilgisi.get("durum", arac_bilgisi["fiyat"])
        ctk.CTkLabel(kutu, text=durum_yazisi, font=("Roboto", 11), text_color="gray").pack(pady=0)
        
        if "tarih" in arac_bilgisi:
            ctk.CTkLabel(
                kutu, 
                text=arac_bilgisi["tarih"], 
                font=("Roboto", 10), 
                text_color="#0D0D0E" 
            ).pack(pady=(0, 0))
       
        iade_et = None
        if buton_text == "İADE ET":
            
            iade_et = lambda a=arac_bilgisi: self.iade_et_islemi(a)
       
        ctk.CTkButton(
            kutu, 
            text=buton_text, 
            fg_color=renk_tema, 
            height=22, 
            width=90, 
            font=("Roboto", 10, "bold"),
            command=iade_et
        ).pack(pady=(5, 8))
    
    
    def verileri_yukle(self):
        self.aktif_kiralamalar = []
        self.gecmis_kiralamalar = []
        

        base_path = os.path.dirname(os.path.abspath(__file__))
        car_json_yolu = os.path.join(base_path, "..", "data", "car.json")

        if os.path.exists(car_json_yolu):
            with open(car_json_yolu, "r", encoding="utf-8") as f:
                tum_araclar = json.load(f)
                
            this_user_id = str(self.current_user.get("id"))

            for arac in tum_araclar:
             
                if str(arac.get("rented_id")) == this_user_id:
                    kart_verisi = {
                        "marka": arac.get("brand", ""),
                        "model": arac.get("model", ""),
                        "fiyat": f"{arac.get('price', 0)} ₺",
                        "resim": f"{arac.get('brand', '').lower()}.png",
                        "durum": f"Teslim: {arac.get('finsh_date', '?')}",
                        "tarih": f"{arac.get('start_date', '')} - {arac.get('finsh_date', '')}"
                    }
                    self.aktif_kiralamalar.append(kart_verisi)

        gecmis_listesi = self.current_user.get("history", [])
        
        for gecmis_arac in gecmis_listesi:
            
            self.gecmis_kiralamalar.append(gecmis_arac)




    def iade_et_islemi(self, arac_bilgisi):
        onay = messagebox.askyesno("İade Onayı", f"{arac_bilgisi['marka']} {arac_bilgisi['model']} iade edilsin mi?")
        
        if onay:
            base_path = os.path.dirname(os.path.abspath(__file__))
            car_json_yolu = os.path.join(base_path, "..", "data", "car.json")
            user_json_yolu = os.path.join(base_path, "..", "data", "user.json")
            
            if os.path.exists(car_json_yolu):
                with open(car_json_yolu, "r", encoding="utf-8") as f:
                    araclar = json.load(f)
                
                arac_bulundu = False
                for arac in araclar:
                   
                    if (arac["brand"] == arac_bilgisi["marka"] and 
                        arac["model"] == arac_bilgisi["model"] and 
                        str(arac.get("rented_id")) == str(self.current_user.get("id"))):
                        
                      
                        arac["status"] = "Müsait"
                        arac["rented_id"] = None
                        arac["start_date"] = None
                        arac["finsh_date"] = None
                        arac_bulundu = True
                        break
                
                if arac_bulundu:
                    with open(car_json_yolu, "w", encoding="utf-8") as f:
                        json.dump(araclar, f, ensure_ascii=False, indent=4)
            
          
            if os.path.exists(user_json_yolu):
                with open(user_json_yolu, "r", encoding="utf-8") as f:
                    kullanicilar = json.load(f)
                
                for user in kullanicilar:
                   
                    if str(user["id"]) == str(self.current_user["id"]):
                        
                        # Eğer 'history' listesi yoksa oluştur
                        if "history" not in user:
                            user["history"] = []
                        
                       
                        bugun = datetime.now().strftime("%d.%m.%Y")
                        gecmis_veri = arac_bilgisi.copy()
                        gecmis_veri["durum"] = "Kiralama Tamamlandı"
                        gecmis_veri["tarih"] = f"İade Tarihi: {bugun}"
                        
                        user["history"].append(gecmis_veri)
                        
                      
                        if "history" not in self.current_user:
                            self.current_user["history"] = []
                        self.current_user["history"].append(gecmis_veri)
                        
                        break
                
                with open(user_json_yolu, "w", encoding="utf-8") as f:
                    json.dump(kullanicilar, f, ensure_ascii=False, indent=4)

            
            messagebox.showinfo("Başarılı", "Araç iade edildi.")
            self.verileri_yukle() 
            self.listeleri_ciz() 

    

    def musteri_sayfasina_git(self):
        from ui.customerPage import MusteriSayfasi
        self.destroy()
        app = MusteriSayfasi(self.master, self.controller, self.db_manager, self.current_user)
        app.grid(row=0, column=0, sticky="nsew")

    def bilgileri_guncelle(self):
       
        yeni_veriler = {
            "name": self.entry_widgets["Ad"].get(),
            "surname": self.entry_widgets["Soyad"].get(),
            "age": self.entry_widgets["Yaş"].get(),
            "phone": self.entry_widgets["Tel No"].get(),
            "mail": self.entry_widgets["Gmail"].get(),
            "password": self.entry_widgets["Şifre"].get()
        }

        ana_klasor = os.getcwd()

        dosya_yolu = os.path.join(ana_klasor, "data", "user.json")

        try:
            if not os.path.exists(dosya_yolu):
                messagebox.showerror("Hata", f"Dosya bulunamadı!\nAranan yol:\n{dosya_yolu}")
                return

            with open(dosya_yolu, "r", encoding="utf-8") as f:
                kullanicilar = json.load(f)

            kullanici_bulundu = False
            mevcut_mail = self.current_user.get("mail")

            for user in kullanicilar:
                if user.get("mail") == mevcut_mail:
                    user.update(yeni_veriler)
                    kullanici_bulundu = True
                    break

            if kullanici_bulundu:
                with open(dosya_yolu, "w", encoding="utf-8") as f:
                    json.dump(kullanicilar, f, ensure_ascii=False, indent=4)

                self.current_user.update(yeni_veriler)
                messagebox.showinfo("Başarılı", "Bilgileriniz güncellendi!")
            else:
                messagebox.showerror("Hata", "Kullanıcı dosyada bulunamadı.")

        except Exception as e:
            messagebox.showerror("Hata", f"Hata: {e}")

