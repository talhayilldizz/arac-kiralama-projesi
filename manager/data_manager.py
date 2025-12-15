import json
import os
from models.car import Car
from models.user import User


class Data_Manager:
    def __init__(self):
        self.userfile = 'data/user.json'
        self.carfile = 'data/car.json'

        # Klasör yoksa oluştur
        if not os.path.exists('data'):
            os.makedirs('data')

        if not os.path.exists(self.userfile):
            with open(self.userfile, "w", encoding="utf-8") as f:
                json.dump([], f)

        if not os.path.exists(self.carfile):
            with open(self.carfile, "w", encoding="utf-8") as f:
                json.dump([], f)

    def get_all_users(self):
        with open(self.userfile, "r", encoding="utf-8") as f:
            return json.load(f)

    def user_register(self, id, name, surname, password, age, mail, phone):
        user = User(id, name, surname, password, age, mail, phone).to_dict()

        with open(self.userfile, "r", encoding="utf-8") as f:
            users = json.load(f)

        users.append(user)

        with open(self.userfile, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

        return True

    def user_login(self, mail, password):
        users = self.get_all_users()
        for user in users:
            if user.get('mail') == mail and user.get('password') == password:
                return user
        return False

    # --- ARAÇ İŞLEMLERİ ---

    def get_all_cars(self):
        with open(self.carfile, "r", encoding="utf-8") as f:
            return json.load(f)

    def add_car(self, brand, model, year, plate, price):
        # Yeni araç eklerken varsayılan değerleri de ekleyelim ki json düzgün olsun
        car_dict = Car(brand, model, year, plate, price).to_dict()

        # Car modelinde bu alanlar yoksa manuel ekleyelim
        if "status" not in car_dict: car_dict["status"] = "Müsait"
        if "rented_id" not in car_dict: car_dict["rented_id"] = None
        if "start_date" not in car_dict: car_dict["start_date"] = None
        if "finsh_date" not in car_dict: car_dict["finsh_date"] = None  # Senin json yapına uyumlu (i eksik)

        cars = self.get_all_cars()
        cars.append(car_dict)

        with open(self.carfile, "w", encoding="utf-8") as f:
            json.dump(cars, f, indent=4, ensure_ascii=False)

        return True

    def update_car(self, current_plate, new_plate, brand, model, year, price):
        cars = self.get_all_cars()
        update_cars = []
        updated = False

        for car in cars:
            if car['plate'] == current_plate:
                car['plate'] = new_plate
                car['brand'] = brand
                car['model'] = model
                car['year'] = year
                car['price'] = price
                updated = True
            update_cars.append(car)

        if updated:
            with open(self.carfile, "w", encoding="utf-8") as f:
                json.dump(update_cars, f, indent=4, ensure_ascii=False)
            return True
        return False

    def car_delete(self, plate):
        cars = self.get_all_cars()
        new_cars = []
        deleted = False

        for car in cars:
            # Status kontrolü yaparken büyük küçük harf hatasını önlemek için .lower()
            stat = car.get('status', 'Müsait')
            is_available = stat.lower() == 'müsait' or stat == "Müsait"

            if car['plate'] == plate and is_available:
                deleted = True
                continue
            else:
                new_cars.append(car)

        if deleted:
            with open(self.carfile, "w", encoding="utf-8") as f:
                json.dump(new_cars, f, indent=4, ensure_ascii=False)
            return True
        else:
            return False

    def get_car_by_id(self, plate):
        cars = self.get_all_cars()
        for car in cars:
            if car["plate"] == plate:
                return car
        return None
    
    def get_car_by_mail(self,mail):
        rented_cars = []
        all_cars = self.get_all_cars() 
        
        for car in all_cars:
            if car.get('rented_id') == mail:
                rented_cars.append(car)
                
        return rented_cars
        


    def rent_car(self, plate, user_id, start_date, finish_date):
        cars = self.get_all_cars()
        updated = False

        for car in cars:
            db_plate = str(car.get('plate', '')).strip()
            target_plate = str(plate).strip()

            if db_plate == target_plate:
                print("DEBUG: Araç bulundu, durumu güncelleniyor...")
                car['status'] = "Kirada"
                car['rented_id'] = user_id
                car['start_date'] = start_date
                car['finsh_date'] = finish_date
                updated = True
                break

        if updated:
            try:
                with open(self.carfile, "w", encoding="utf-8") as f:
                    json.dump(cars, f, indent=4, ensure_ascii=False)
                print("DEBUG: Dosya başarıyla kaydedildi.")
                return True
            except Exception as e:
                print(f"DEBUG: Dosya yazma hatası: {e}")
                return False
        else:
            print(f"DEBUG: HATA - {plate} plakalı araç listede bulunamadı!")
            return False