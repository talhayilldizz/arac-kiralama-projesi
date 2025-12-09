class User:
    def __init__(self,id,name,surname,password,age,mail,phone,role="musteri"):
        self.id=id
        self.name=name
        self.surname=surname
        self.passwrod=password
        self.age=age
        self.mail=mail
        self.phone=phone
        self.role=role

    def to_dict(self):
        return{
            "id":self.id,
            "name":self.name,
            "surname":self.surname,
            "password":self.passwrod,
            "age":self.age,
            "mail":self.mail,
            "phone":self.phone,
            "role":self.role
        }
        