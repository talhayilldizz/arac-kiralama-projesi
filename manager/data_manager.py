import json
import os
from models.car import Car
from models.user import User

class Data_Manager:
    def __init__(self):
        self.userfile='data/user.json'
        self.carfile='data/car.json'

        if not os.path.exists(self.userfile):
            with open(self.userfile, "w") as f:
                json.dump([],f)

        if not os.path.exists(self.carfile):
            with open(self.carfile, "w") as f:
                json.dump([], f)

        

    #Kullanıcı İşlemleri

    #Tüm kullanıcıları getir
    def get_all_users(self):
        with open(self.userfile,"r",encoding="utf-8") as f:
            return json.load(f)


    #Register
    def user_register(self,id,name,surname,password,age,mail,phone):

        #Register sayfasından gelen verileri User classına sırasıyla yazıp
        #to_dict fonksiyonu ile json formatına çevirdim
        user=User(id,name,surname,password,age,mail,phone).to_dict()

        #User dosyasındaki tüm verileri çektim
        with open(self.userfile,"r",encoding="utf-8") as f:
            users=json.load(f)

        #Registerdan gelen değerleri atadığım user fonksiyonunu yukarıda çektipim kullanıcı dosyasına ekledim
        users.append(user)

        #Ve kullanıcı dosyasını yazma modunda açıp son halini yazdım
        with open(self.userfile, "w",encoding="utf-8") as f:
            json.dump(users,f,indent=4,ensure_ascii=False)

        return True

    def user_login(self, mail, password):
        users=self.get_all_users()

        # 2. Listeyi döngüye alıp eşleşen kullanıcı var mı diye bakıyoruz
        for user in users:
            # Sözlük içindeki mail ve şifre alanlarını kontrol ediyoruz
            if user.get('mail') == mail and user.get('password') == password:
                # Eşleşme bulunduysa, giriş yapan kullanıcının tüm bilgilerini döndürürüz.
                 return user

        # 3. Döngü biter ve eşleşme bulunamazsa (veya şifre yanlışsa) başarısız demektir
        return False



    #Araç İşlemleri
    def get_all_cars(self):
        with open(self.carfile, "r",encoding="utf-8") as f:
            return json.load(f)
    
    def add_car(self,brand ,model, year,plate, price):
        car=Car(brand,model,year,plate,price).to_dict()
        
        cars=self.get_all_cars()

        cars.append(car)

        with open(self.carfile, "w",encoding="utf-8") as f:
            json.dump(cars,f,indent=4,ensure_ascii=False)

        return True
    
    def update_car(self,current_plate,new_plate,brand,model,year,price):
        cars=self.get_all_cars()
        update_cars=[]

        for car in cars:
            if car['plate'] == current_plate:
                car['plate'] =new_plate
                car['brand']=brand
                car['model']=model
                car['year']=year
                car['price']=price

            update_cars.append(car)

        with open(self.carfile,"w", encoding="utf-8") as f:
            json.dump(update_cars, f, indent=4,ensure_ascii=False)

        return True 
    
    def car_delete(self,plate):
        cars=self.get_all_cars()
        new_cars=[]
        deleted=False

        for car in cars:
            is_car_to_delete = car['plate'] == plate
            is_available = car.get('status', 'Müsait') == 'Müsait'

            if is_car_to_delete and is_available:
                deleted=True
                continue
            else:
                new_cars.append(car)

        if deleted:
            with open(self.carfile,"w",encoding="utf-8") as f:
                json.dump(new_cars,f,indent=4,ensure_ascii=False)
            return True
        else:
            return False

    #plakaya göre o aracı getirme
    def get_car_by_id(self,plate):
        cars=self.get_all_cars()

        for car in cars:
            if car["plate"] == plate:
                return car




        