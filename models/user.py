class User:
    def __init__(self, id, name, surname, password, age, mail, phone, role="musteri"):
        self.__id = id
        self.name = name
        self.surname = surname

        # Private Değişkenler
        self.__password = password
        self.__age = age
        self.__mail = mail
        self.__phone = phone

        self.role = role

    # getter
    @property
    def id(self):
        return self.__id

    @property
    def password(self):
        return self.__password

    @property
    def age(self):
        return self.__age

    @property
    def mail(self):
        return self.__mail

    @property
    def phone(self):
        return self.__phone


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "password": self.__password,
            "age": self.__age,
            "mail": self.__mail,
            "phone": self.__phone,
            "role": self.role
        }