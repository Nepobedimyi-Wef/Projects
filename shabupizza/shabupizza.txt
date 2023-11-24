n = 1
Basket = []
while n >= 1 and n < 5:
    def menu_1(menu):
        menu = ("\n 1 - Перейти к меню "
                "\n 2 - Оплата"              
                "\n 3 - Корзина"
                "\n 4 - Редактирование корзины"              
                "\n 5 - Выход")
        return menu
    print(menu_1(1))
    Action_selection = int(input("Введите цифру желаемого действия:"))

    def go_to_order_1 (go_to_order):
        menu_2 = ("\n 1 - Пицца 350 рублей"
                  "\n 2 - Шаурма 280 рублей"
                  "\n 3 - Кола 100 рублей ")
        print(menu_2)
        go_to_order_2 = int(input("Введите цифру товара который желаете заказать:"))


        if go_to_order_2 == 1:
            Basket.append("Пицца")
        elif go_to_order_2 == 2:
            Basket.append('Шаурма')
        elif go_to_order_2 == 3:
            Basket.append('Кола')


    def payment_1(payment):
        Total_price = Basket.count('Кола') * 100 + Basket.count('Шаурма') * 280 + Basket.count('Пицца') * 350
        print("Вы купили товаров на сумму: ", Total_price)
        print(('\n Введите способ оплаты:\n 1 - по карте \n 2 - наличными '))
        sposob_oplaty = int(input())
        if sposob_oplaty == 2:
            Bill_for_payment = int(input("Введите сумму оплаты наличными: "))
            if Bill_for_payment > Total_price:
                print("Вот ваша сдача:", Bill_for_payment - Total_price)
                print("Спасибо за покупку")
            elif Bill_for_payment == Total_price:
                print("Спасибо за покупку")
            else:
                print("Вы дали недостаточную сумму для оплаты заказа")
        if sposob_oplaty == 1:
            print("Спасибо за покупку")

    def cart_1(cart):
        print('Кола:', Basket.count('Кола'), "Цена:", Basket.count('Кола') * 100)
        print('Шаурма:', Basket.count('Шаурма'), "Цена:", Basket.count('Шаурма') * 280)
        print('Пицца:', Basket.count('Пицца'), "Цена:", Basket.count('Пицца') * 350)
        Total_price = Basket.count('Кола') * 100 + Basket.count('Шаурма') * 280 + Basket.count('Пицца') * 350
        print("Итого: ", Total_price)


    def editing_cart_1(editing_cart):
        print('Кола колличество:', Basket.count('Кола'), "Цена:", Basket.count('Кола') * 100)
        print('Шаурма колличество:', Basket.count('Шаурма'), "Цена:", Basket.count('Шаурма') * 280)
        print('Пицца колличество:', Basket.count('Пицца'), "Цена:", Basket.count('Пицца') * 350)
        Total_price = Basket.count('Кола') * 100 + Basket.count('Шаурма') * 280 + Basket.count('Пицца') * 350
        print("Итого: ",Total_price)
        print("Хотите изменить колличество Колы?\n 0 - уменьшить , 1 - оставить прежним, 2 - увеличить")
        number = int(input())
        if number == 0:
            number_1 = int(input("Впешите колличество на которое хотите уменьшить: "))
            while number_1 > 0:
                Basket.remove('Кола')
                number_1 = number_1 - 1
        if number == 2:
            number_1 = int(input("Впешите колличество на которое хотите увеличить: "))
            while number_1 > 0:
                Basket.append('Кола')
                number_1 = number_1 - 1
        print("Хотите изменить колличество Шаурмы?\n 0 - уменьшить , 1 - оставить прежним, 2 - увеличить")
        number = int(input())
        if number == 0:
            number_1 = int(input("Впешите колличество на которое хотите уменьшить: "))
            while number_1 > 0:
                Basket.remove('Шаурма')
                number_1 = number_1 - 1
        if number == 2:
            number_1 = int(input("Впешите колличество на которое хотите увеличить: "))
            while number_1 > 0:
                Basket.append('Шаурма')
                number_1 = number_1 - 1
        print("Хотите изменить колличество Пиццы?\n 0 - уменьшить , 1 - оставить прежним, 2 - увеличить")
        number = int(input())
        if number == 0:
            number_1 = int(input("Впешите колличество на которое хотите уменьшить: "))
            while number_1 > 0:
                Basket.remove('Пицца')
                number_1 = number_1 - 1
        if number == 2:
            number_1 = int(input("Впешите колличество на которое хотите увеличить: "))
            while number_1 > 0:
                Basket.append('Пицца')
                number_1 = number_1 - 1
        print('Кола колличество:', Basket.count('Кола'), "Цена:", Basket.count('Кола') * 100)
        print('Шаурма колличество:', Basket.count('Шаурма'), "Цена:", Basket.count('Шаурма') * 280)
        print('Пицца колличество:', Basket.count('Пицца'), "Цена:", Basket.count('Пицца') * 350)
        Total_price = Basket.count('Кола') * 100 + Basket.count('Шаурма') * 280 + Basket.count('Пицца') * 350
        print("Итого: ", Total_price)


    if Action_selection == 1:
        go_to_order_1("go_to_order")
    elif Action_selection == 2:
        payment_1("payment")
    elif Action_selection == 3:
        cart_1("cart")
    elif Action_selection == 4:
        editing_cart_1("editing_cart")
    elif Action_selection == 5:
        print("До свидания!")
        break