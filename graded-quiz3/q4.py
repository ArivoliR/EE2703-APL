
def timer(func):
    def wrapper():
	      return func()
    return wrapper

def func(x):
    print(x)
x = 10
print(timer(func(x)))
