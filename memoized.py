import functools
import sys
import dis
import time

def memoized(func = None, *, enable=False):
    if func is None:
        return lambda func: memoized(func, enable=enable)
    mem = {}
    
    @functools.wraps(func)
    def inner(*args, **kwargs):
        key = args + tuple(sorted(kwargs.items()))
        print(key)
        print(mem)
        if enable:
            if key not in mem:
                print('hello')
                mem[key] = func(*args, **kwargs)
        else:
            mem[key] = func(*args, *kwargs)
            print(func.__name__, args, kwargs, mem)
        print(mem)
        return mem[key]
    return inner
 
@memoized(enable=True)
def uselles(*args):
    l = [i*2 for i in args]
    return sum(l)

print(uselles(2, 4, 4, 4, 6))