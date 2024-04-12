import random
s = input("Введите строку: ")
s = s.replace(' ', '')
characters = list(s)
binary_string = ''.join(format(ord(char), '08b') for char in characters)
while len(binary_string) % 3 != 0:
    binary_string += '0'
a1 = ['апельсин', 'автомобиль', 'аптека']
b1 = ['банан', 'бутерброд', 'библиотека']
c1 = ['жираф', 'живот', 'желание']
d1 = ['йогурт', 'йод', 'йога']
e1 = ['медведь', 'море', 'машина']
f1 = ['птица', 'песок', 'печь']
g1 = ['тигр', 'тюльпан', 'тетрадь']
h1 = ['холодильник', 'хомяк', 'хлеб']
j1 = ['шарф', 'шоколад', 'школа']
k1 = ['электричество', 'эхо', 'экран']
output_words = []
while binary_string:
    group = binary_string[:3]
    if group == '000':
        output_words.append(random.choice(a1))
    elif group == '001':
        output_words.append(random.choice(b1))
    elif group == '010':
        output_words.append(random.choice(c1))
    elif group == '011':
        output_words.append(random.choice(d1))
    elif group == '100':
        output_words.append(random.choice(e1))
    elif group == '101':
        output_words.append(random.choice(f1))
    elif group == '110':
        output_words.append(random.choice(g1))
    elif group == '111':
        choice_list = random.choice([h1, j1, k1])
        output_words.append(random.choice(choice_list))
    binary_string = binary_string[3:]
print(' '.join(output_words))
