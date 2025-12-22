import json
import os
from models.car import Car
from models.user import User


class Data_Manager:
    def __init__(self):
        self.__userfile = 'data/user.json'
        self.__carfile = 'data/car.json'

        # Klasör yoksa oluştur
        if not os.path.exists('data'):
            os.makedirs('data')

        if not os.path.exists(self.__userfile):
            with open(self.__userfile, "w", encoding="utf-8") as f:
                json.dump([], f)

        if not os.path.exists(self.__carfile):
            with open(self.__carfile, "w", encoding="utf-8") as f:
                json.dump([], f)

    def get_all_users(self):
        with open(self.__userfile, "r", encoding="utf-8") as f:
            return json.load(f)

    def user_register(self, id, name, surname, password, age, mail, phone):
        user = User(id, name, surname, password, age, mail, phone).to_dict()
        user["history"]=[]

        with open(self.__userfile, "r", encoding="utf-8") as f:
            users = json.load(f)

        users.append(user)

        with open(self.__userfile, "w", encoding="utf-8") as f:
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
        with open(self.__carfile, "r", encoding="utf-8") as f:
            return json.load(f)

    def add_car(self, brand, model, year, plate, price):
        # Yeni araç eklerken varsayılan değerleri de ekleyelim ki json düzgün olsun
        car_dict = Car(brand, model, year, plate, price).to_dict()

        # Car modelinde bu alanlar yoksa manuel ekleyelim
        if "status" not in car_dict: car_dict["status"] = "Müsait"
        if "rented_id" not in car_dict: car_dict["rented_id"] = None
        if "start_date" not in car_dict: car_dict["start_date"] = None
        if "finsh_date" not in car_dict: car_dict["finsh_date"] = None  

        cars = self.get_all_cars()
        cars.append(car_dict)

        with open(self.__carfile, "w", encoding="utf-8") as f:
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
            with open(self.__carfile, "w", encoding="utf-8") as f:
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
            with open(self.__carfile, "w", encoding="utf-8") as f:
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
    
    def get_car_by_mail(self, mail):
        cars=self.get_all_cars()
        rented_cars=[]
        for car in cars:
            if car['rented_id'] == mail:
                rented_cars.append(car)
        
        return rented_cars

        


    def rent_car(self, plate, user_mail, start_date, finish_date):
       
        cars = self.get_all_cars()
        car_found = None
        
        for car in cars:
            if car.get('plate') == plate:
                car['status'] = "Kirada"
                car['rented_id'] = user_mail
                car['start_date'] = start_date
                car['finsh_date'] = finish_date
                car_found = car # Arabayı hafızaya aldık, aşağıda kullanacağız
                break
        
        if not car_found:
            return False

        users = self.get_all_users()
        user_updated = False

        # Geçmişe eklenecek veriler
        history_record = {
            "plate": plate,
            "year": car_found.get('year', '-'),
            "brand": car_found['brand'],
            "model": car_found['model'],
            "start_date": start_date,
            "finsh_date": finish_date,
            "price": car_found['price'],
            "status": "Aktif" 
        }

        for user in users:
            if user['mail'] == user_mail: 
                if "history" not in user:
                    user["history"] = [] # Eski kullanıcılarda hata vermesin diye kontrol
                
                user["history"].append(history_record)
                user_updated = True
                break
        
        if user_updated:
              
            with open(self.__carfile, "w", encoding="utf-8") as f:
               json.dump(cars, f, indent=4, ensure_ascii=False)
            with open(self.__userfile, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=4, ensure_ascii=False)

          
            return True
            
        return False
    
    def return_car(self, plate):
       
        cars = self.get_all_cars()
        rented_user_mail = None 
        car_found = False

        for car in cars:
            if car.get('plate') == plate:
                rented_user_mail = car.get('rented_id') 
                
                car['status'] = "Müsait"
                car['rented_id'] = None
                car['start_date'] = None
                car['finsh_date'] = None
                car_found = True
                break
        
        if not car_found:
            print("HATA: Araç veritabanında bulunamadı.")
            return False

        users = self.get_all_users()
        history_updated = False
        
        if rented_user_mail:
            for user in users:
                
                if user.get('mail') == rented_user_mail:
                    if "history" in user:
                        for record in reversed(user["history"]): #en guncel kaydı bulmak için tersten bakıyoruz
                            if record["plate"] == plate and record.get("status") == "Aktif":
                                record["status"] = "Tamamlandı"
                                history_updated = True
                                break 
                    break

        try:
            
            with open(self.__carfile, "w", encoding="utf-8") as f:
                json.dump(cars, f, indent=4, ensure_ascii=False)
            
            if history_updated:
                with open(self.__userfile, "w", encoding="utf-8") as f:
                    json.dump(users, f, indent=4, ensure_ascii=False)
          
            return True

        except Exception as e:
            print(f"HATA: Dosya kaydetme hatası: {e}")
            return False