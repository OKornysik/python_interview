import functools
import sys
import dis

def trace(func=None, *, handle=sys.stdout):
    if func is None:
        return lambda func: trace(func, handle=handle)
    
    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(func.__name__, args, kwargs)
        return func(*args, **kwargs)
    return inner
 
@trace        
def uselles(x):
    return x

uselles(42)
dis.dis(trace)