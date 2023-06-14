__all__ = ["Product", "Tshirt", "Hoodie"]

class Product:
    def __init__(self, name, size, color, image):
        self.name = name
        self.size = size
        self.color = color
        self.image = image

    def getName(self):
        return self.name
    
    def getSize(self):
        return self.size
    
    def getColor(self):
        return self.color
    
    def getImage(self):
        return self.image
    
    def setName(self, name):
        self.name = name

    def setSize(self, size):
        self.size = size

    def setColor(self, color):
        self.color = color

class Tshirt(Product):
    def __init__(self, name, size, color, image, price):
        super().__init__(name, size, color, image)
        self.price = price

    def getPrice(self):
        return self.price
    
    def setPrice(self, price):
        self.price = price

    def to_dict(self):
        return {"name": self.name, "size": self.size, "color": self.color, "image": self.image, "price": self.price}
    
class Hoodie(Product):
    def __init__(self, name, size, color, image, price):
        super().__init__(name, size, color, image)
        self.price = price

    def getPrice(self):
        return self.price
    
    def setPrice(self, price):
        self.price = price

    def to_dict(self):
        return {"name": self.name, "size": self.size, "color": self.color, "image": self.image, "price": self.price}