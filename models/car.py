class Car:
    def __init__(self,brand,model,year,plate,price,status="Müsait",rented_id=None,start_date=None,finsh_date=None):
        self.brand=brand
        self.model=model
        self.year=year
        self.plate=plate
        self.price=price
        self.status=status
        self.rented_id=rented_id
        self.start_date=start_date
        self.finsh_date=finsh_date

    def to_dict(self):
        return {
            "brand":self.brand,
            "model":self.model,
            "year":self.year,
            "plate":self.plate,
            "price":self.price,
            "status":self.status,
            "rented_id":self.rented_id,
            "start_date":self.start_date,
            "finsh_date":self.finsh_date
        }