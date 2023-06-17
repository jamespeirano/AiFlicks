__all__ = ["Product", "Tshirt", "Hoodie"]

class Product:
    _id = 1

    def __init__(self, name, size, color, image, price, quantity=1):
        self.id = Product._id
        Product._id += 1
        self.name = name
        self.size = size
        self.color = color
        self.image = image
        self.price = price
        self.quantity = quantity

    @property
    def quantity(self):
        return self._quantity
    
    @quantity.setter
    def quantity(self, quantity):
        self._quantity = quantity

    def to_dict(self):
        return {"id": self.id, "name": self.name, "size": self.size, "color": self.color, "image": self.image, "price": self.price, "quantity": self.quantity}

class Tshirt(Product):
    pass

class Hoodie(Product):
    pass