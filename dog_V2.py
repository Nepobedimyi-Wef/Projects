 class Person:
    def __init__(self, name, age, color, breed, weight):
        self.__name = name  # устанавливаем имя
        self.__age = age  # устанавливаем возраст
        self.__color = color # устанавливаем цвет
        self.__breed = breed # устанавливаем породу
        self.__weight = weight # устанавливаем вес

    # свойство-геттер
    @property
    def age(self):
        return self.__age

    # свойство-сеттер
    @age.setter
    def age(self, age):
        if 0 < age < 50:
            self.__age = age
        else:
            print("Недопустимый возраст")
    @property
    def weight(self):
        return self.__weight
    @weight.setter
    def weight(self, weight):
        if 1 < weight < 100:
            self.__weight = weight
        else:
            print("Недопустимый вес")

    @property
    def name(self):
        return self.__name

    def print_person(self):
        if 0 < Age < 50 and 1 < Weight < 100:
            print(f"Имя: {self.__name}\tВозраст: {self.__age}\tЦвет: {self.__color}\tПорода: {self.__breed}\tВес: {self.__weight}")
Name = input('Введите имя собаки: ')
Age = int(input('Введите возраст собаки: '))
Color = input('Введите цвет собаки: ')
Breed = input('Введите породу собаки: ')
Weight = int(input('Введите вес собаки: '))
tom = Person(Name,'', Color, Breed, '')
tom.age = Age
tom.weight = Weight
tom.print_person()
