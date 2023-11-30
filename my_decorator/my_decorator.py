def multiply(func):
    def wrapper(a,b):
        result = func(a,b)
        return result*2
    return wrapper
@multiply
def add_numbers(a,b):
    return a+b
print(add_numbers(25,21))
