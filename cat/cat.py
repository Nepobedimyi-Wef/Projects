class Animal:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def name(self):
        return self.__name

    def display_name(self):
        print(f"Name: {self.__name}",f"\nAge: {self.__age} ")


class Cat(Animal):

    def say(self):
        print(f"{self.name} say: meow")


tom = Cat("Tom",10)
tom.display_name()
tom.say()
