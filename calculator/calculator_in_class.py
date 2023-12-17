final = 1
class calculator:
    def addition(self, num1, num2):
        print(num1 + num2)

    def subtraction(self, num1, num2):
        print(num1 - num2)

    def multiplication(self, num1, num2):
        print(num1 * num2)

    def division(self, num1, num2):
        print(num1 / num2)

while 1 == final:
    try:
        try:
            num1 = int(input('Введите первое число: '))
            num2 = int(input('Введите второе число: '))
            calculator = calculator()
            while True:
                action = input('Введите символ действия с числами из этих + - * /\n')
                if '+' == action:
                    calculator.addition(num1,num2)
                    break
                elif '-' == action:
                    calculator.subtraction(num1,num2)
                    break
                elif '*' == action:
                    calculator.multiplication(num1,num2)
                    break
                elif '/' == action:
                    calculator.division(num1,num2)
                    break
                else:
                    print('Вы ввели некоректный символ!')
            while True:
                end = input('Вы хотите выключить калькулятор?\n')
                if end == 'Да' or end == 'ДА' or end == 'да':
                    print('Досвидания')
                    final = 0
                    break
                else:
                    break
        except(ZeroDivisionError):
            print('На ноль делить нельзя!')
    except(ValueError):
        print('Ненадо писать буквы или пропуски за место чисел!')
