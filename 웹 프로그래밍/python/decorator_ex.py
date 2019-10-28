def hello(func):
    def wrapper():
        print("hi hi")
        func()
        print("hi hi hi")
    return wrapper

@hello    # bye()가 hello()에 func으로 들어가게 된다
def bye():
    print("bye bye")

bye()