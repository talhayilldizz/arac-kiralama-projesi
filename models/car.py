class Car:
    def __init__(self,brand,model,plate,price,is_rented="Müsait",rented_id=None,start_date=None,finsh_date=None):
        self.brand=brand
        self.model=model
        self.plate=plate
        self.price=price
        self.is_rented=is_rented
        self.rented_id=rented_id
        self.start_date=start_date
        self.finsh_date=finsh_date

    def to_dict(self):
        return {
            "brand":self.brand,
            "model":self.model,
            "plate":self.plate,
            "is_rented":self.is_rented,
            "rented_id":self.rented_id,
            "start_date":self.start_date,
            "finsh_date":self.finsh_date
        }