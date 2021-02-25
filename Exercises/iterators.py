ds = (1, 2, 3, 4)
print(ds.__iter__())
print(range(10))

def g():
    print('start')
    x = 42
    print('stop before 1st yield')
    yield x
    print('start afrer 1st yield')
    x += 1
    print('stop before 2nd yield')
    yield x
    print('start afrer 2nd yield')
    print('programm done')
    yield 
    
gen = g()
print(next(gen))
print('----------')
print(next(gen))
print('----------')
print(next(gen))
