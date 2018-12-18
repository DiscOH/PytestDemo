def do_twice(func):
    def wrapper_do_twice(arg):
        func(arg)
        func(arg)
    return wrapper_do_twice


@do_twice
def append_cat(a):
    a.append('cat')


herd = list()

append_cat(herd)

print(herd)