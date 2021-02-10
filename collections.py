## ---------- TUPLE ----------

# Литералы кортежа — обычные скобки, почти всегда их можно и нужно опускать:
point = (1, 2)
x, y = point
date = "October", 5
# НО
z = (0, )
print(x, y, z, date)

person = ("George", "Carlin", "May", 12, 1937)
name, birthday = person[:2], person[2:]
print(name, birthday)

b, c = [1, 2], [3, 4]
a = b, c # создали кортеж, сам он не изменяемый, но листы внутри - изменяемы. Тоесть внутри кортежа линки на обьекты списки
print(a, id(a))
b.append(7) # изменили список внутри коретжа - айдишник не меняется
print(a, id(a))

print((1, 2, 3)[::-1]) # создает новый кортеж
print(list(reversed((1, 2, 3)))) # reversed создает итератор, а не копию кортежа. Когда нужно проитерироваться - лучше использовать reversed

xs, ys = (1, 2), (3, )
print(id(xs), id(ys))
print(xs + ys, id(xs + ys)) # Результатом конкатенации всегда является новый кортеж

print((1, 2, 3) < (1, 2, 4)) # Сравнение кортежей происходит в лексикографическом порядке
print((1, 2, 3, 4) < (1, 2, 4))
print((1, 2) < (1, 2, 42))

# from collections import namedtuple
# Person = namedtuple("Person", ["name", "age"])# Функция namedtuple возвращает тип кортежа, специализированный на фиксированное множество полей
# print(p = Person("George", age=77))
# print(p._fields)
# print(p.name, p.age)
# print(p._asdict())
# print(p._replace(name="Bill"))

## ---------- LIST ----------

chunks = [[0]] * 2 # матрица 2 x 1 из нулей
print(chunks)
chunks[0][0] = 42 # копируем ссылку на изменяемый обьек, список хешбл. С интами и строками так можно
print(chunks)
chunks = [[0] for i in range(2)] # нужно делат так, использовать генератор списков
print(chunks) 

# Методы append и extend добавлют в конец списка один элемент или произвольную последовательность соответственно:
xs = [1, 2, 3]
xs.append(42) # ==> [1, 2, 3, 42]
print(xs) 
xs.extend({-1, -2}) # ==> [1, 2, 3, 42, -2, -1]
print(xs)
# Вставить элемент перед элементом с указанным индексом можно с помощью метода insert:
xs = [1, 2, 3]
xs.insert(0, 4) # ==> [4, 1, 2, 3]
print(xs)
xs.insert(-1, 42) # ==> [4, 1, 2, 42, 3]
print(xs)
# Можно также заменить подпоследовательность на элементы другой последовательности:
xs = [1, 2, 3]
xs[:2] = [0] * 2 # ==> [0, 0, 3]
print(xs)
xs = [1, 2, 3, 4, 5]
ys = [7, 8]
xs[1:4] = ys # ==> [1, 7, 8, 5]
print(xs)

# Конкатенация списков работает аналогично конкатенации кортежей: результатом всегда является новый список
# В отличие от кортежей списки поддерживают inplace конкатенацию:
print(xs, id(xs))
xs += ys # ≈ xs = xs.extend(ys)
print(xs, id(xs))

del xs[:2] # удаляет со списка элепент или последовательность и ничего не возвращает
xs.pop(-1) # удаляет элемент по индексу и взвращает его

xs = [1, 2, 3, 2]
xs.remove(2) # удаляет первое вхождение элемента по значению
print(xs)

xs = [1, 2, 3]
print(list(reversed(xs))) # создаем новый список с помощью полученого итератора
xs.reverse() # переворачивает список inplace, не создавая новый, возвращает None
print(xs)

# аналогично работает с функией sorted(xs) и методом xs.sort()

# Функции sorted и методу sort можно опционально указать направление сортировки, а также функцию-ключ
xs = [3, 2, 1]
xs.sort(key=lambda x: x % 2, reverse=True)
print(xs)

# Тип deque реализует двустороннюю очередь

# from collections import deque
# q = deque()
# q = deque([1, 2, 3])
# q.appendleft(0) # -> deque([0, 1, 2, 3])
# q.append(4) # -> deque([0, 1, 2, 3, 4])
# q.popleft() # -> 0
# q[0] # -> 1
# q = deque([1, 2], maxlen=2) # При добавлении элемента к ограниченной очереди лишние элементы “вываливаются” с противоположной стороны

## ---------- SET ----------

xs, ys, zs = {1, 2}, {2, 3}, {3, 4}
print(xs, ys, zs)
print(xs | ys, xs - ys, xs & ys, xs <= ys)

seen = set()
for i in range(1, 4):
    seen.add(i) # Добавить один элемент
seen.update([8], [9], [(1, 2)]) # добавить последовательность элементов
print(seen)

seen.remove(3) # удаляет из множества существующий элемент или поднимает исключение, если элемент во множестве не содержится
print(seen)
seen.discard(100500) # удаляет элемент, если есть и не подымает исключение если нет
kek = frozenset() # создает неизменяемое множество; можно делать почти все то же, кроме добавления и удаления элементов

## ---------- DICT ----------

d = dict(foo="bar")
c = dict(d) # (shallow) копия
print(c)
dict(d, boo="baz") # копирование с добавлением ключей

d = {'a': 1, 'b': 2, 'c': 3}
print(d.keys(), d.values(), d.items()) # Методы keys, values и items возвращают проекции содержимого словаря

# Проекции поддерживают стандратные операции последовательности (len, in / not in, etc)
# Проекция keys дополнительно реализует некоторые операции множества (&, |, etc)
# Модифицировать содержимое словаря в процесс итерации нельзя
# Если очень хочется, можно сделать копию проекции и итерироваться по ней

for k in set(d):
	del d[k]
print(d)

d = {'k': 1, 'l': 2}
c = {x for x in d.values()}
print(d, c, type(d), type(c))
print(d['k'], d.get('k'), d.get('nope', 42))
d['nope'] = 42
print(d)

# Метод setdefault позволяет за один запрос к хеш-таблице проверить, есть ли в ней значение по ключу и, если значения нет - установить его в заданное

print(d.setdefault("k", "???"), d.setdefault("boo", 42))

del d['k']
d.pop('boo')
print(d)
d.clear()
print(d)

# from collections import defaultdict
# g = defaultdict(set, **{"a": {"b"}, "b": {"c"}})
# g["c"].add("a")

# OrderedDict — словарь с ключами, упорядоченными по времени добавления
# 	from collections import OrderedDict
# 	d = OrderedDict([("foo", "bar"), ("boo", 42)])
# 	list(d) -> ['foo', 'boo']

# Тип Counter — это специализация словаря для подсчёта объектов, которые можно захешировать
# 	from collections import Counter
# 	c = Counter(["foo", "foo", "foo", "bar"])
# 	c["foo"] += 1
# 	print(c) -> Counter({'foo': 4, 'bar': 1})

# Метод elements перечисляет элементы счётчика в произвольном порядке. Элементы, для которых частота равна нулю или отрицательна, игнорируются
# 	c = Counter(foo=4, bar=-1)
# 	list(c.elements()) -> ['foo', 'foo', 'foo', 'foo']
# Метод most_common возвращает заданное число самых частых элементов
# 	c.most_common(1) -> [('foo', 4)]
# Методы substract и update позволяют поэлементно обновить значения счётчика
# 	c.update(["bar"])
# 	c -> Counter({'foo': 4, 'bar': 0})
#	c.subtract({"foo": 2})
#	c -> Counter({'foo': 2, 'bar': 0})

# Можно использовать heapq (куча), чтобы находить самые большие и маленькие итемы. Также можно запилить коллекцию с приоритетами
from collections.abc import Iterable

def flatten(items, ignore = (str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore):
            yield from flatten(x)
        else:
            yield x
            
            
a = [1, 2, [3, 4, [5, 6], 7]]
print(list(flatten(a)))
