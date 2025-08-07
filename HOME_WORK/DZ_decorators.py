import functools
import sys

# 1.
def check_division_error(func):
    @functools.wraps(func)
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except ZeroDivisionError:
            print("Помилка! Ділення на ноль не можливе!")
            sys.exit()
    return wrapper
# 2.
def check_index_error(func):
    @functools.wraps(func)
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except IndexError:
            print("Помилка, невідповідний індекс!")
            sys.exit()
    return wrapper

# 3.
@check_division_error
def divide(a, b):
    return a / b

# 4.
@check_index_error
def get_element(new_list, index):
    return new_list[index]

# 5.
print(divide(80, 2))
print(divide(46, 12))
print(divide(0, 12))
#print(divide(8, 0))

# Після виникнення помилки (ділення на 0) функція divide
# викликає sys.exit(), тому виконання програми завершується.
# Щоб перевірити роботу другого декоратора (get_element),
# необхідно тимчасово закоментувати виклики divide, які викликають помилки.

print(get_element([2, 4, 8, 4, 5], 2))
print(get_element([2, 8, 19, 7], 5))