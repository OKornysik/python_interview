class Noop:
    some_attribute = 42
    _another = 'gfh'
    __stop = 0, 1, 3
    def __init__(self):
        self.value = 3
        self.__stop = [7, 8, 9]
    
c = Noop()
print(Noop.some_attribute, Noop._another, Noop._Noop__stop) # Noop.value -> AttributeError: type object 'Noop' has no attribute 'value'
print(c.some_attribute, c._another, c._Noop__stop, c.value)

# class A:
#     def f(self):
#         print('im A')

# class B(A):
#     def f(self):
#         print('im B')
#        super().f()

# print(isinstance(B(), A))
# print(issubclass(B, A))

# class C(B):
#     def f(self):
#         print('im C')
#         super().f()

# c = C()
# c.f()

#print(C.mro())

import functools

# deco for class method
def deprecated(cls):
    def_init = cls.__init__
    
    @functools.wraps(cls.__init__)
    def new_init(self, *args, **kwargs):
        print(cls.__name__ + ' is deprecated')
        def_init(self, *args, **kwargs)
    
    cls.__init__ = new_init
    return cls

@deprecated    
class A:
    def __init__(self):
        print('im fine')
a = A()

# deco for class attribute
def deprecated(cls):
    old_value = cls.value
    new_value = 'useless'
    cls.value = new_value
    return cls

@deprecated    
class A:
    value = 'valuable'
    def get_value(self):
        print(self.value)
        return self.value
    
A().get_value()


        
