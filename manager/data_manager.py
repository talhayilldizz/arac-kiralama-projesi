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
        with open(self.userfile,"r") as f:
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


        