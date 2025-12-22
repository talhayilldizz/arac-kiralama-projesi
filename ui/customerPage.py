import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import tkinter.messagebox as messagebox


class KiralaPopup(ctk.CTkToplevel):
    def __init__(self, parent, arac_bilgisi, db, current_user_mail):
        super().__init__(parent)
        self.title("Araç Kiralama Onayı")
        self.geometry("400x550")
        self.resizable(False, False)

        self.db = db
        self.user_mail = current_user_mail

        self.attributes("-topmost", True)
        self.grab_set()

        self.arac = arac_bilgisi

        # Araç Adı Belirleme
        marka = arac_bilgisi.get("brand", arac_bilgisi.get("marka", ""))
        model = arac_bilgisi.get("model", "")
        self.arac_adi = f"{marka} {model}"

        # Fiyatı Sayıya Çevirme
        ham_fiyat = arac_bilgisi.get("price", arac_bilgisi.get("fiyat", 0))
        try:
            fiyat_str = str(ham_fiyat).replace("₺", "").replace("TL", "").replace(".", "").strip()
            self.gunluk_fiyat = int(fiyat_str)
        except:
            self.gunluk_fiyat = 0

        ctk.CTkLabel(self, text=f"{self.arac_adi}", font=("Roboto", 22, "bold"), text_color="#2C3E50").pack(
            pady=(20, 5))
        ctk.CTkLabel(self, text=f"Günlük: {self.gunluk_fiyat} TL", font=("Roboto", 14), text_color="gray").pack(
            pady=(0, 15))

        # Tarih Seçimi
        ctk.CTkLabel(self, text="Alış Tarihi:", font=("Roboto", 14, "bold")).pack(pady=5)
        self.cal_baslangic = DateEntry(self, width=12, background='#2C3E50', foreground='white', borderwidth=2,
                                       date_pattern='dd.mm.yyyy')
        self.cal_baslangic.pack(pady=5)

        ctk.CTkLabel(self, text="İade Tarihi:", font=("Roboto", 14, "bold")).pack(pady=5)
        self.cal_bitis = DateEntry(self, width=12, background='#2C3E50', foreground='white', borderwidth=2,
                                   date_pattern='dd.mm.yyyy')
        self.cal_bitis.pack(pady=5)

        # Hesapla Butonu
        ctk.CTkButton(self, text="Fiyat Hesapla", command=self.hesapla, fg_color="#E67E22").pack(pady=20)

        # Sonuç Göstergesi
        self.lbl_sonuc = ctk.CTkLabel(self, text="Toplam: 0 Gün\nTutar: 0 TL", font=("Roboto", 18, "bold"),
                                      text_color="#27AE60")
        self.lbl_sonuc.pack(pady=10)

        # Onay Butonu
        ctk.CTkButton(self, text="KİRALAMAYI TAMAMLA", command=self.kirala_onayla, fg_color="#27AE60", height=45,
                      font=("Roboto", 14, "bold")).pack(side="bottom", pady=30, padx=20, fill="x")

    def hesapla(self):
        t1 = self.cal_baslangic.get_date()
        t2 = self.cal_bitis.get_date()

        if t2 < t1:
            messagebox.showerror("Hata", "İade tarihi, alış tarihinden önce olamaz!")
            return None

        gun_sayisi = (t2 - t1).days
        if gun_sayisi <= 0: gun_sayisi = 1  # En az 1 gün

        toplam_tutar = gun_sayisi * self.gunluk_fiyat

        self.lbl_sonuc.configure(text=f"Toplam: {gun_sayisi} Gün\nTutar: {toplam_tutar} TL")
        return toplam_tutar

    def kirala_onayla(self):
        tutar = self.hesapla()

        if tutar:
            plaka = self.arac.get("plate")
            start_date = self.cal_baslangic.get_date().strftime("%d.%m.%Y")
            finish_date = self.cal_bitis.get_date().strftime("%d.%m.%Y")

            # Data_Manager içindeki rent_car fonksiyonu çalışacak
            basari = self.db.rent_car(plaka, self.user_mail, start_date, finish_date)

            if basari:
                messagebox.showinfo("Başarılı", f"{self.arac_adi} başarıyla kiralandı!")

                if hasattr(self.master, 'listele'):
                    self.master.listele()
                elif hasattr(self.master, 'verileri_yukle_ve_goster'):
                    self.master.verileri_yukle_ve_goster()

                self.destroy()
            else:
                messagebox.showerror("Hata", "Kiralama kaydedilemedi! Lütfen yöneticiye bildirin.")


class DetayPopup(ctk.CTkToplevel):
    def __init__(self, parent, arac_bilgisi):
        super().__init__(parent)
        self.title("Araç Durum Detayı")
        self.geometry("350x400")
        self.resizable(False, False)

        self.attributes("-topmost", True)
        self.grab_set()


        marka = arac_bilgisi.get("brand", "")
        model = arac_bilgisi.get("model", "")
        ad = f"{marka} {model}"


        baslangic = arac_bilgisi.get("start_date", "-")
        bitis = arac_bilgisi.get("finsh_date", "-")  # Senin JSON yapındaki 'finsh' typo'su korundu

        header_frame = ctk.CTkFrame(self, fg_color="#E67E22", corner_radius=0, height=60)
        header_frame.pack(fill="x")

        ctk.CTkLabel(header_frame, text="ARAÇ KİRADA", font=("Roboto", 20, "bold"), text_color="white").place(relx=0.5,
                                                                                                              rely=0.5,
                                                                                                              anchor="center")
        # Araç Bilgisi
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(content_frame, text=ad, font=("Roboto", 22, "bold"), text_color="#2C3E50").pack(pady=(10, 20))

        # Tarih Bilgileri Kutusu
        info_box = ctk.CTkFrame(content_frame, fg_color="#ECF0F1", corner_radius=10)
        info_box.pack(fill="x", pady=10, ipady=10)

        ctk.CTkLabel(info_box, text="Kiralama Başlangıç:", font=("Roboto", 12), text_color="#7F8C8D").pack(pady=(10, 0))
        ctk.CTkLabel(info_box, text=baslangic, font=("Roboto", 16, "bold"), text_color="#2C3E50").pack(pady=(0, 10))

        ctk.CTkFrame(info_box, height=1, fg_color="#BDC3C7").pack(fill="x", padx=30, pady=5)

        ctk.CTkLabel(info_box, text="Tahmini Dönüş:", font=("Roboto", 12), text_color="#7F8C8D").pack(pady=(10, 0))
        ctk.CTkLabel(info_box, text=bitis, font=("Roboto", 16, "bold"), text_color="#C0392B").pack(pady=(0, 10))

        # Kapat Butonu
        ctk.CTkButton(self, text="Kapat", command=self.destroy, fg_color="#34495E", width=120).pack(side="bottom",
                                                                                                    pady=30)

import customtkinter as ctk



class MusteriSayfasi(ctk.CTkFrame):
    def __init__(self, parent, controller, db_manager, current_user=None):
        super().__init__(parent, fg_color="#ECF0F1")
        self.controller = controller
        self.__db = db_manager
        self.__current_user = current_user

        # Grid Ayarları
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


        self.entry_marka = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Marka Ara...",
            height=40,
            font=("Roboto", 14),
            fg_color="#34495E",
            text_color="#ECF0F1",
            placeholder_text_color="#7F8C8D",
            border_width=0
        )
        self.entry_marka.grid(row=2, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.entry_model = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Model Ara...",
            height=40,
            font=("Roboto", 14),
            fg_color="#34495E",
            text_color="#ECF0F1",
            placeholder_text_color="#7F8C8D",
            border_width=0
        )
        self.entry_model.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.opt_fiyat = ctk.CTkComboBox(
            self.sidebar,
            values=["Fiyat Aralığı", "0 - 1500 TL", "1500 - 3000 TL", "3000+ TL"],
            height=40,
            font=("Roboto", 14),
            fg_color="#34495E",
            text_color="#ECF0F1",
            button_color="#34494E",
            border_width=0,
            button_hover_color="#2C3E50",
            dropdown_fg_color="#34495E",
            dropdown_text_color="white"
        )
        self.opt_fiyat.set("Fiyat Aralığı")
        self.opt_fiyat.grid(row=4, column=0, padx=20, pady=(0, 15), sticky="ew")

        self.btn_uygula = ctk.CTkButton(
            self.sidebar,
            text="Listele",
            fg_color="#1ABC9C",
            height=50,
            font=("Roboto", 15, "bold"),
            hover_color="#16A085",
            command=self.listele
        )
        self.btn_uygula.grid(row=5, column=0, padx=20, pady=30, sticky="ew")


        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)


        self.top_bar = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.top_bar.pack(fill="x", pady=(10, 10))

        ctk.CTkLabel(
            self.top_bar,
            text="ARAÇ LİSTESİ",
            font=("Roboto", 24, "bold"),
            text_color="#2C3E50"
        ).pack(side="left", pady=5)

        self.profil_menu = ctk.CTkOptionMenu(
            self.top_bar,
            values=["Profilim", "Çıkış Yap"],
            width=140,
            fg_color="#2C3E50",
            corner_radius=8,
            command=self.profile_git
        )
        self.profil_menu.set(f"👤 Hesabım")
        self.profil_menu.pack(side="right")


        self.main_scroll = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.main_scroll.pack(fill="both", expand=True)


        self.musait_grid_frame = None
        self.kirada_grid_frame = None
        self.bakimda_grid_frame = None


        self.verileri_yukle_ve_goster()

    def verileri_yukle_ve_goster(self):
        self.musait_araclar = []
        self.kirada_olanlar = []


        try:
            tum_araclar = self.__db.get_all_cars()
        except Exception as e:
            print(f"Veri çekme hatası: {e}")
            tum_araclar = []

        for arac in tum_araclar:
            durum = arac.get("status", "").lower()

            # Fiyat düzenlemesi
            fiyat = str(arac.get("price", "0"))
            if "₺" not in fiyat and "TL" not in fiyat:
                fiyat += " TL"
            arac["display_price"] = fiyat

            if "müsait" in durum:
                self.musait_araclar.append(arac)
            elif "kirada" in durum:
                self.kirada_olanlar.append(arac)

        # Arayüzü Temizle
        for widget in self.main_scroll.winfo_children():
            widget.destroy()

        # Müsait araç olmasa bile başlığı gösteriyoruz
        self.musait_grid_frame = self.bolum_olustur(baslik="MÜSAİT ARAÇLAR", renk="#27AE60",
                                                    arac_listesi=self.musait_araclar)
        ctk.CTkFrame(self.main_scroll, height=2, fg_color="#BDC3C7").pack(fill="x", pady=20, padx=10)

        # Kirada araç olmasa bile başlığı gösteriyoruz
        self.kirada_grid_frame = self.bolum_olustur(baslik="KİRADA OLANLAR", renk="#E67E22",
                                                    arac_listesi=self.kirada_olanlar)

    def bolum_olustur(self, baslik, renk, arac_listesi):
        baslik_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        baslik_frame.pack(fill="x", pady=(5, 10))

        ctk.CTkFrame(baslik_frame, width=6, height=28, fg_color=renk, corner_radius=4).pack(side="left", padx=(10, 10))
        ctk.CTkLabel(baslik_frame, text=f"{baslik} ({len(arac_listesi)})", font=("Roboto", 18, "bold"),
                     text_color="#2C3E50").pack(side="left")

        grid_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        grid_frame.pack(fill="both")


        for i in range(4):
            grid_frame.grid_columnconfigure(i, weight=1)

        # Eğer liste boşsa uyarı yazısı, doluysa kartları ekle
        if not arac_listesi:
            ctk.CTkLabel(grid_frame, text="Bu kategoride araç bulunmamaktadır.", text_color="gray",
                         font=("Roboto", 12, "italic")).grid(row=0, column=0, columnspan=4, pady=10)
        else:
            self.araclari_grid_doldur(grid_frame, arac_listesi, renk)

        return grid_frame

    def araclari_grid_doldur(self, parent_frame, liste, renk):
        for i, arac in enumerate(liste):
            row = i // 4
            col = i % 4
            self.kart_ekle(parent_frame, row, col, arac, renk)

    def kart_ekle(self, parent, r, c, arac_bilgisi, renk_tema):
        kutu = ctk.CTkFrame(parent, fg_color="white", corner_radius=12, border_color="#BDC3C7", border_width=1)
        kutu.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
        kutu.grid_rowconfigure(0, weight=1)  # İçerik dikeyde esnesin


        content_frame = ctk.CTkFrame(kutu, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)


        full_name = f"{arac_bilgisi.get('brand', '')} {arac_bilgisi.get('model', '')}"
        ctk.CTkLabel(
            content_frame,
            text=full_name,
            font=("Roboto", 16, "bold"),
            text_color="#2C3E50",
            wraplength=150
        ).pack(anchor="w")


        yil = arac_bilgisi.get('year', '-')

        plaka = arac_bilgisi.get('plate', '---')
        ctk.CTkLabel(
            content_frame,
            text=f"{yil} | {plaka}",
            font=("Roboto", 12),
            text_color="#7F8C8D"
        ).pack(anchor="w", pady=(2, 10))


        ctk.CTkFrame(content_frame, height=2, fg_color="#F0F3F4").pack(fill="x", pady=5)


        fiyat = arac_bilgisi.get("display_price", "0 TL")
        ctk.CTkLabel(
            content_frame,
            text=fiyat,
            font=("Roboto", 18, "bold"),
            text_color=renk_tema
        ).pack(pady=(10, 5))


        durum = arac_bilgisi.get("status", "").lower()
        musait_mi = "müsait" in durum

        btn_text = "KİRALA" if musait_mi else "DETAY"

        komut = None
        if musait_mi:
            komut = lambda: self.popup_ac(arac_bilgisi)
        else:
            komut = lambda: self.detay_popup_ac(arac_bilgisi)

        ctk.CTkButton(
            content_frame,
            text=btn_text,
            fg_color="#2C3E50" if musait_mi else "#95A5A6",
            height=35,
            width=120,
            font=("Roboto", 13, "bold"),
            command=komut,
            corner_radius=8
        ).pack(pady=(10, 0), side="bottom")

    def listele(self):
        try:
            araclar = self.__db.get_all_cars()
        except:
            araclar = []

        self.musait_araclar = []
        self.kirada_olanlar = []

        for arac in araclar:
            durum = str(arac.get("status", "")).lower()
            
            fiyat = str(arac.get("price", "0"))
            if "₺" not in fiyat and "TL" not in fiyat:
                fiyat += " TL"
            arac["display_price"] = fiyat

            if "müsait" in durum:
                self.musait_araclar.append(arac)
            elif "kirada" in durum:
                self.kirada_olanlar.append(arac)

    
        girilen_marka = self.entry_marka.get().strip().lower()
        girilen_model = self.entry_model.get().strip().lower()
        secilen_fiyat = self.opt_fiyat.get()

        filtrelenmis_musait = []

        for arac in self.musait_araclar:
           
            marka = str(arac.get("brand", "")).strip().lower()
            model = str(arac.get("model", "")).strip().lower()

            fiyat = str(arac.get("price", "0")).replace("₺", "").replace("TL", "").strip()
            try:
                fiyat_int = int(fiyat)
            except:
                fiyat_int = 0

            marka_uygun = (not girilen_marka) or (girilen_marka in marka)
            model_uygun = (not girilen_model) or (girilen_model in model)

            fiyat_uygun = False
            if secilen_fiyat == "Fiyat Aralığı":
                fiyat_uygun = True
            elif secilen_fiyat == "0 - 1500 TL" and 0 <= fiyat_int <= 1500:
                fiyat_uygun = True
            elif secilen_fiyat == "1500 - 3000 TL" and 1500 <= fiyat_int <= 3000:
                fiyat_uygun = True
            elif secilen_fiyat == "3000+ TL" and fiyat_int >= 3000:
                fiyat_uygun = True

            if marka_uygun and model_uygun and fiyat_uygun:
                filtrelenmis_musait.append(arac)

        #Ekrana yazdırma
        
        if self.musait_grid_frame is not None:
            for widget in self.musait_grid_frame.winfo_children():
                widget.destroy()

            for i in range(4): self.musait_grid_frame.grid_columnconfigure(i, weight=1)

            if not filtrelenmis_musait:
                ctk.CTkLabel(self.musait_grid_frame, text="Kriterlere uygun araç bulunamadı.", text_color="#C0392B",
                             font=("Roboto", 14)).grid(row=0, column=0, columnspan=4, pady=20)
            else:
                self.araclari_grid_doldur(self.musait_grid_frame, filtrelenmis_musait, "#27AE60")

        if self.kirada_grid_frame is not None:
            for widget in self.kirada_grid_frame.winfo_children():
                widget.destroy()

            for i in range(4): self.kirada_grid_frame.grid_columnconfigure(i, weight=1)

            if not self.kirada_olanlar:
                ctk.CTkLabel(self.kirada_grid_frame, text="Bu kategoride araç bulunmamaktadır.", text_color="gray",
                             font=("Roboto", 12, "italic")).grid(row=0, column=0, columnspan=4, pady=10)
            else:
                self.araclari_grid_doldur(self.kirada_grid_frame, self.kirada_olanlar, "#E67E22")



    def profile_git(self, secim):
        if secim == "Profilim":
            from ui.profilePage import ProfilSayfasi
            self.destroy()
            app = ProfilSayfasi(self.master, self.controller, self.__db, self.__current_user)
            app.grid(row=0, column=0, sticky="nsew")

        elif secim == "Çıkış Yap":
            from ui.loginPage import LoginPage
            self.destroy()
            app = LoginPage(self.master, self.controller, self.__db)
            app.grid(row=0, column=0, sticky="nsew")

    def popup_ac(self, arac_bilgisi):
        user_mail = self.__current_user['mail'] if isinstance(self.__current_user, dict) else "Misafir"
        KiralaPopup(self, arac_bilgisi, self.__db, user_mail)

    def detay_popup_ac(self, arac_bilgisi):
        DetayPopup(self, arac_bilgisi)