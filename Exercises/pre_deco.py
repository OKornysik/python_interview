import functools
import sys
import dis
import time

def pre(condition, message):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            print(args, kwargs, 'first')
            assert condition(*args, **kwargs), message
            return func(*args, **kwargs)
        return inner
    return wrapper

def post(condition, message):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            print(result, 'second')
            assert condition(result), message
            return result
        return inner
    return wrapper

@pre(lambda *args, key: key != 0, 'dont pick zero as key')
@post(lambda result: result < 100, 'too much')
def dil(*args, key=1):
    c = sum(args)
    return c / key

print(dil(2, 4, 4, 4, 6, key=2))
print(chr(0x68))