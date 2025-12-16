import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class RaporlarSayfasi(ctk.CTkFrame):
    def __init__(self,parent,controller,db_manager):
        super().__init__(parent,fg_color="#ECF0F1")
        self.controller=controller
        self.db=db_manager

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=120)
        self.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(
            self,
            height=140,
            fg_color="#2C3E50",
            corner_radius=0
        )
        self.header_frame.grid(row=0, column=0, sticky="nsew")
        self.header_frame.grid_columnconfigure(1, weight=1)

        # Geri Butonu (ikon hissi)
        self.back_button = ctk.CTkButton(
            self.header_frame,
            text="❮",
            width=42,
            height=42,
            font=("Roboto", 20, "bold"),
            fg_color="#2F3640",
            hover_color="#353B48",
            corner_radius=12,
            command=self.admin_page
        )
        self.back_button.grid(row=0, column=0, padx=25, pady=30, sticky="w")

        # Başlık Alanı
        title_container = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )
        title_container.grid(row=0, column=1, sticky="w")

        self.title_label = ctk.CTkLabel(
            title_container,
            text="Araç Raporları",
            font=("Roboto", 26, "bold"),
            text_color="#F5F6FA"
        )
        self.title_label.pack(anchor="w")

        self.subtitle_label = ctk.CTkLabel(
            title_container,
            text="Kiralama istatistikleri ve gelir analizleri",
            font=("Roboto", 14),
            text_color="#DCDDE1"
        )
        self.subtitle_label.pack(anchor="w")


        # Grafik Alanı
        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#ECF0F1"
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.content_frame.grid_columnconfigure((0,1), weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)


        self.brand_rental_chart()
        self.status_pie_chart()
        self.total_revenue_chart()
        self.revenue_by_brand_chart()
        self.price_distribution_chart()
        self.rentals_by_user_chart()



    #Kullanıcıların geçmiş işlemleri
    def get_all_histories(self):
        users=self.db.get_all_users()
        all_history=[]

        for user in users:
            history=user.get("history",[])
            all_history.extend(history)
        
        return all_history
    
    #Grafikler

    #Kiralanan marka grafiği
    def brand_rental_chart(self):
        brand_count = {}
        for h in self.get_all_histories():
            brand_count[h["brand"]] = brand_count.get(h["brand"], 0) + 1

        card = self.create_card(self.content_frame, "Markaya Göre Kiralama Sayısı")
        card.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.bar(brand_count.keys(), brand_count.values())
        ax.set_ylabel("Adet")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        self._grafik_gom(card, fig)

    #Araçların durumunu belirten grafik
    def status_pie_chart(self):
        status = {"Aktif": 0, "Tamamlandı": 0}
        for h in self.get_all_histories():
            if h["status"] in status:
                status[h["status"]] += 1

        card = self.create_card(self.content_frame, "Kiralama Durumu")
        card.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.pie(status.values(), labels=status.keys(), autopct="%1.0f%%")

        self._grafik_gom(card, fig)

    #Toplam ciro grafiği
    def total_revenue_chart(self):
        total = sum(
            int(h["price"].replace("₺", "").strip())
            for h in self.get_all_histories()
        )

        card = self.create_card(self.content_frame, "Toplam Ciro")
        card.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.bar(["Toplam"], [total])
        ax.set_ylabel("Fiyat")

        self._grafik_gom(card, fig)


    #Hangi marka daha çok ciro yaptırıyo
    def revenue_by_brand_chart(self):
        revenue = {}
        for h in self.get_all_histories():
            price = int(h["price"].replace("₺", "").strip())
            revenue[h["brand"]] = revenue.get(h["brand"], 0) + price

        card = self.create_card(self.content_frame, "Markaya Göre Ciro")
        card.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.bar(revenue.keys(), revenue.values())
        ax.set_ylabel("Fiyat")

        self._grafik_gom(card, fig)

    #Kiralamalar hangi fiyat aralığında
    def price_distribution_chart(self):
        prices = [
            int(h["price"].replace("₺", "").strip())
            for h in self.get_all_histories()
        ]

        card = self.create_card(self.content_frame, "Fiyat Dağılımı")
        card.grid(row=2, column=0, padx=15, pady=15, sticky="nsew")

        fig = plt.Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.hist(prices, bins=5)
        ax.set_xlabel("Fiyat")

        self._grafik_gom(card, fig)

    #En çok kiralama yapan kullanıcılar
    def rentals_by_user_chart(self):
        users = self.db.get_all_users()
        counts = {}
        for u in users:
            if u.get("role") == "musteri":
                name = f'{u["name"]} {u["surname"][:3]}'
                counts[name] = len(u.get("history", []))

        card = self.create_card(self.content_frame, "Kullanıcı Kiralamaları")
        card.grid(row=2, column=1, padx=15, pady=15, sticky="nsew")

        fig = plt.Figure(figsize=(6, 6))
        ax = fig.add_subplot(111)
        ax.bar(counts.keys(), counts.values())
        ax.tick_params(axis="x", rotation=30)

        self._grafik_gom(card, fig)


    def create_card(self, parent, title):
        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=16
        )
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Roboto", 16, "bold"),
            text_color="#2C3E50"
        )
        title_label.pack(pady=(15,5))

        return card
    
    def _grafik_gom(self, parent, fig):
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()

        widget = canvas.get_tk_widget()
        widget.pack(padx=10, pady=10, fill="both", expand=True)

        plt.close(fig)

    def admin_page(self):
        from ui.adminPage import AdminSayfasi
        import matplotlib.pyplot as plt

        for w in self.content_frame.winfo_children():
            w.destroy()

        plt.close("all")
        self.content_frame.destroy()
        self.destroy()
        AdminSayfasi(
            self.master,
            self.controller,
            self.db
        ).pack(expand=True, fill="both")

