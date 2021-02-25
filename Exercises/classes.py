import functools

class Noop:
    some_attribute = 42 # запись атрибута класса, есть у всех екземпляров этого класса, может перегружаться
    _another = 'gfh'
    __stop = 0, 1, 3
    def __init__(self): # конструктор класса
        self.value = 3 # запись атрибута екземпляра
        self.__stop = [7, 8, 9] # перегружаем атрибут __stop для екземпляров
    
c = Noop()
print(Noop.some_attribute, Noop._another, Noop._Noop__stop) # Noop.value -> AttributeError: type object 'Noop' has no attribute 'value'
print(c.some_attribute, c._another, c._Noop__stop, c.value)

print(Noop.__doc__)
print(Noop.__name__)
print(Noop.__module__)
print(Noop.__bases__)
noop = Noop()
print(noop.__class__)
print(noop.__dict__) # словарь атрибутов объекта
print(noop.some_attribute) # в дикте екземпляра нету, но есть в дикте класса
# Добавление, изменение и удаление атрибутов — это фактически операции со словарём

# С помощью специального аттрибута класса __slots__ можно зафиксировать множество возможных атрибутов экземпляра
class Noop:
    __slots__ = ["some_attribute"]

noop = Noop()
noop.some_attribute = 42
print(noop.some_attribute) # -> 42
# noop.some_other_attribute = 100500 -> AttributeError: 'Noop' object has no attribute [...]
# Экземпляры класса с указанным __slots__ требуют меньше памяти, потому что у них отсутствует __dict__

class SomeClass:
    def do_something(self):
        print("Doing something.")

SomeClass().do_something # связанный
SomeClass().do_something() # -> Doing something.

SomeClass.do_something # несвязанный
instance = SomeClass()
SomeClass.do_something(instance) # -> Doing something.

# Механизм свойств позволяет объявлять атрибуты, значение которых вычисляется в момент обращения
class Path:
    def __init__(self, current):
        self.current = current

    def __repr__(self):
        return "Path({})".format(self.current)
    
    @property 
    def parent(self): # Такое свойство не записуется в дикт присоздании екземпляра, а вычисляется при обращении
        return Path(dirname(self.current))

p = Path("./examples/some_file.txt")
print(p.parent) # -> Path('./examples')

# Можно также переопределить логику изменения и удаления таких атрибутов

class BigDataModel:
    def __init__(self):
        self._params = []
    
    @property
    def params(self):
        return self._params
    
    @params.setter
    def params(self, new_params):
        assert all(map(lambda p: p > 0, new_params))
        self._params = new_params
    
    @params.deleter
    def params(self):
        del self._params
    
model = BigDataModel()
model.params = [0.1, 0.5, 0.4]
print(model.params) # -> [0.1, 0.5, 0.4]

# ---------- Наследование ----------

# Вообще конструкция функции super() состоит из класса и екземпляра, типо super(class, instance)...
# Когда ничего не вписываем, типо super(), туда подставляется класс в котором мы находимся, и екземпляр
# В случае множественного наследования Python использует алгоритм линеаризации C3 для определения метода, который нужно вызвать
class A:
    def f(self):
        print('im A')

class B(A):
    def f(self):
        print('im B')
        super().f() # Вызывает функцию f() у класса по иерархии выше, в нашем случае у класса А

print(isinstance(B(), A))
print(issubclass(B, A))

class C(B):
    def f(self):
        print('im C')
        super().f()

c = C()
c.f()
print(C.mro())

# ---------- Классы-примеси ----------

# Классы-примеси позволяют выборочно модифицировать поведение класса в предположении, что класс реализует некоторый интерфейс
class Counter:
    def __init__(self, value):
        self.value = value

    def increment(self):
        self.value += 1

    def get(self):
        return self.value

class ThreadSafeMixin:
    
    def increment(self):
        print('im added')
        super().increment()

    def get(self):
        print('im also')
        super().get()
    
class DefaultCounter(Counter):
    pass

a = DefaultCounter(42)
print(a.get())
a.increment()
print(a.get())

class ThreadSafeCounter(ThreadSafeMixin, Counter):
    pass

a = ThreadSafeCounter(42)
print(a.get())
a.increment()
print(a.get())

# ---------- Декораторы ----------

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

# ---------- Магические методы ----------

# Магическими” называются внутренние методы классов, например, метод __init__
# С помощью “магических” методов можно
#   • управлять доступом к атрибутам экземпляра
#   • перегрузить операторы, например, операторы сравнения или арифметические операторы
#   • определить строковое представление экземпляра или изменить способ его хеширования

# Метод __getattr__ вызывается при попытке прочитать значение несуществующего атрибута        
class Noop:
    def __getattr__(self, name): # перегрузили __getattr__ чтобы возвращал имя аргумента который мы пытались получить
        return name # identity

Noop().foobar # -> 'foobar'

# Методы __setattr__ и __delattr__ позволяют управлять изменением значения и удалением атрибутов
# В отличие от __getattr__ они вызываются для всех атрибутов, а не только для несуществующих
# Пример, запрещающий изменять значение некоторых атрибутов
class Guarded:
    guarded = []
    
    def __setattr__(self, name, value):
        assert name not in self.guarded
        super().__setattr__(name, value)
    
class Noop(Guarded):
    guarded = ["foobar"]

    def __init__(self):
        self.__dict__["foobar"] = 42

class Noop:
    some_attribute = 42
    
noop = Noop()
getattr(noop, "some_attribute") # -> 42
getattr(noop, "some_other_attribute", 100500) # -> 100500
# Комплементарные функции setattr и delattr добавляют и удаляют атрибут
setattr(noop, "some_other_attribute", 100500)
delattr(noop, "some_other_attribute")

# Метод __call__ позволяет “вызывать” экземпляры классов, имитируя интерфейс фнукций
class Identity:
    def __call__(self, x):
        return x

Identity()(42) # -> 42

# - “Магические” методы позволяют уточнить поведение экземпляров класса в различных конструкциях языка
# - Например, с помощью магического метода __str__ можно указать способ приведения экземпляра класса, а с
#   помощью метода __hash__ — алгоритм хеширования состояния класса
# - Мы рассмотрели небольшое подмножество “магических” методов, на самом деле их много больше: практически
#   любое действие с экземпляром можно специализировать для конкретного класса
