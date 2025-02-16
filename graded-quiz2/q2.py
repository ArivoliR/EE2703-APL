def double_output(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 2
    return wrapper

@double_output
def add_five(x):
    return x + 5

print(add_five(10))
