class User:
    def __init__(self,id,name,surname,password,age,mail,phone):
        self.id=id
        self.name=name
        self.surname=surname
        self.passwrod=password
        self.age=age
        self.mail=mail
        self.phone=phone

    def to_dict(self):
        return{
            "id":self.id,
            "name":self.name,
            "surname":self.surname,
            "password":self.passwrod,
            "age":self.age,
            "mail":self.mail,
            "phone":self.phone
        }
        