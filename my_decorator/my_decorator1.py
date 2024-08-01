def multiply(func):
    def wrapper(a,b):
        result = func(a,b)
        return result*2
    return wrapper
@multiply
def add_num(a,b):
    return a+b
print(add_num(50,100))
