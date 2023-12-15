class Person:

    def __init__(self, name):
        self.name = name  # имя человека
        self.age = 21  # возраст человека
        self.weight = 80 # вес человека
        self.height = 180 # высота человека
        self.width = 50 # ширина от спины до живота человека
        self.length = 60 # ширина от плеча до плеча человека
        self.waist = 80 # объём талии человека
        self.biceps_volume = 40 # объём бицепса человека
        self.leg_volume = 60 # объём ноги человека
        self.jump_length = 250 # длина прыжка человека
        self.jump_height_with_height = 260 # высота прыжка с ростом человека

tom = Person("Tom")
print(tom.name)
print(tom.age)
print(tom.weight)
print(tom.height)
print(tom.width)
print(tom.length)
print(tom.waist)
print(tom.biceps_volume)
print(tom.leg_volume)
print(tom.jump_length)
print(tom.jump_height_with_height)
