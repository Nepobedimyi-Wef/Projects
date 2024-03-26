class multiplication:
    def multiplitcation(self, num):
        print(num * 3)

class minus:
    def minus(self, num):
        print(num - 2)
class chek(multiplication, minus):
    pass
number = chek()
number.minus(5)
number.multiplitcation(5)
