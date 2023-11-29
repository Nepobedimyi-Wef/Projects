multiply = 1
division = 2
addition = 3
subtraction = 4
end = 5
action_end = 0
while True:
    try:
        if action_end == end:
            print('Калькулятор выключен')
            break    
    except ValueError as e:
        print("Всё заново")
        break    
    except ZeroDivisionError as e:
        print("Всё заново")
        break    
    while True:
        try:
            number_1 = int(input('Введите первое число:'))
            number_2 = int(input('Введите второе число:'))
        except ValueError as e:
            print("Всё заново")
            break        
        except ZeroDivisionError as e:
            print("Всё заново")
            break        
            print('Выберите действие написав число: 1: умножить 2: разделить 3: сложение 4: вычитание')
        try:
            action = int(input())
        except ValueError as e:
            print("Всё заново")
            break        
        except ZeroDivisionError as e:
            print("Всё заново")
            break        
        try:
            if action == multiply:
                print(number_1 * number_2)
            if action == division:
                print(number_1 / number_2)
            if action == addition:
                print(number_1 + number_2)
            if action == subtraction:
                print(number_1 - number_2)
        except ValueError as e:
            print("Всё заново")
            break        
        except ZeroDivisionError as e:
            print("Всё заново")
            break        
            print('Выключить калькулятор?Да:5 Нет:6')
        try:
            action_end = int(input())
        except ValueError as e:
            print("Всё заново")
            break        
        except ZeroDivisionError as e:
            print("Всё заново")
            break        
        try:
            if action_end == end:
                break        
        except ValueError as e:
            print("Всё заново")
            break        
        except ZeroDivisionError as e:
            print("Всё заново")
            break
