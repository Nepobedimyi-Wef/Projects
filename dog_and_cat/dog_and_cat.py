import abc


class Animal(abc.ABC):
    @abc.abstractmethod
    def animal(self): pass


class Cat(Animal):
    def __init__(self,  name, age):
        self.name = name
        self.age = age

    def animal(self):
        if 0 < age <= 40:
            return print(f"Cat name: {self.name} \nAge: {self.age} \nSay: Meow")
        else:
            return print('Некоректный возраст')

class Dog(Animal):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def animal(self):
        if 0 < age <= 50:
            return print(f"Dog name: {self.name} \nAge: {self.age} \nSay: Bark")
        else:
            return print('Некоректный возраст')

def Info(Animal):
    Animal.animal()

name = input('Введите имя кота: ')
age = int(input('Введите возраст кота: '))
name1 = input('Введите имя собаки: ')
age1 = int(input('Введите возраст собаки: '))
cat = Cat(name, age)
dog = Dog(name1, age1)
Info(cat)
Info(dog)
