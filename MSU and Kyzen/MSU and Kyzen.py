import abc
class Computer(abc.ABC):
    @abc.abstractmethod
    def computer(self): pass


class MSU(Computer):
    def __init__(self,  model, аccessories, price):
        self.model = model
        self.аccessories = аccessories
        self.price = price

    def computer(self):
        if 0 < price:
            return print(f"MSU model: {self.model} \nАccessories: {self.аccessories} \nPrice: {self.price}")
        else:
            return print('Некоректная цена')

class Kyzen(Computer):
    def __init__(self,  model, аccessories, price):
        self.model = model
        self.аccessories = аccessories
        self.price = price

    def computer(self):
        if 0 < price:
            return print(f"Kyzen model: {self.model} \nАccessories: {self.аccessories} \nPrice: {self.price}")
        else:
            return print('Некоректная цена')


def Info(Computer):
    Computer.computer()

model = input('Введите модель msu: ')
аccessories = input('Введите комплектующие msu: ')
price = int(input('Введите цену msu: '))
model1 = input('Введите модель kyzen: ')
аccessories1 = input('Введите комплектующие kyzen: ')
price1 = int(input('Введите цену kyzen: '))
msu = MSU(model, аccessories, price)
kyzen = Kyzen(model1, аccessories1, price1)
Info(msu)
Info(kyzen)
