class PriceControl:
    '''Descriptor class to check if a parameter is in range (0,100)'''
    def __set_name__(self, owner, name):
        self.name = name
        
    def __set__(self, instance, value):
        if 0 <= value <= 100:
            instance.__dict__[self.name] = value
        else:
            raise ValueError(f'{self.name.capitalize()} must be between 0 and 100')

class NameControl:
    '''Descriptor class that forbids resetting a parametter once it's set'''
    def __set_name__(self, owner, name):
        self.name = name
        
    def __set__(self, instance, value):
        if self.name in instance.__dict__:
            raise ValueError(f'{self.name.capitalize()} cannot be changed')
        else:
            instance.__dict__[self.name] = value

class Book:
    author = NameControl()
    name = NameControl()
    price = PriceControl()
    
    def __init__(self, author, name, price):
        self.author = author
        self.name = name
        self.price = price
