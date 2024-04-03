import abc
class Car(abc.ABC):
    @abc.abstractmethod
    def car(self): pass


class Coyota(Car):
    def __init__(self,  model, year, price):
        self.model = model
        self.year = year
        self.price = price

    def car(self):
        if 1885 < year <= 2024 and 0 < price:
            return print(f"Coyota model: {self.model} \nYear: {self.year} \nPrice: {self.price}")
        else:
            return print('Некоректный год или цена')

class VMW(Car):
    def __init__(self,  model, year, price):
        self.model = model
        self.year = year
        self.price = price

    def car(self):
        if 1885 < year <= 2024 and 0 < price:
            return print(f"VWM model: {self.model} \nYear: {self.year} \nPrice: {self.price}")
        else:
            return print('Некоректный год или цена')


def Info(Car):
    Car.car()

model = input('Введите имя модель койоты: ')
year = int(input('Введите год выпуска койоты: '))
price = int(input('Введите цену койоты: '))
model1 = input('Введите имя модель вмв: ')
year1 = int(input('Введите год выпуска вмв: '))
price1 = int(input('Введите цену вмв: '))
coyota = Coyota(model, year, price)
vmw = VMW(model1, year1, price1)
Info(coyota)
Info(vmw)
