## Unicode

import sys

a = list(map(ord, "hello"))
print(a)
print(''.join([chr(i) for i in a]))


## Strings method
## doc - https://docs.python.org/3/library/stdtypes.html#string-methodslist(map(ord, "hello"))

print('foo bar'.capitalize())
print('foo bar'.title())
print('foo bar'.upper())
print('foo bar'.lower())
print('foo bar'.capitalize().swapcase())

print('foo bar'.ljust(16, '~'))
print('foo bar'.rjust(16, '~'))
print('foo bar'.center(16, '~'))
print('foo bar'.center(16))

print(']>>foo bar<<['.lstrip('>]'))
print(']>>foo bar<<['.rstrip('<['))
print(']>>foo bar<<['.strip('><]['))
print('\t      foo bar    \r\n   '.strip())

print("foo,bar".split(",")) #Метод split разделяет строку на подстроки по указанному разделителю
print("\t foo bar \r\n ".split())  #Если разделитель не указан, то строка разделяется по пробелам
print("foo,bar,baz".partition(",")) #Метод partition возвращает кортеж из трёх элементов: подстрока до вхождения разделителя, сам разделитель и подстрока после вхождения разделителя

print(", ".join(["foo", "bar", "baz"])) #С помощью метода join можно соединить любую последовательность строк
print(''.join('Hello World!'.split())) # Убирает пробелы из строки

print('foo' in 'foobar')
print('foobar'.startswith('foo'))
print('foobar'.endswith('foo'))

print("abracadabra".find("ra"))
print("abracadabra"[:3])
print("abracadabra".find("ra", 0, 3))
#print("abracadabra".index("ra", 0, 3)) #Метод index аналогичен find, но, если искомая подстрока не найдена, он поднимает исключение

print("abracadabra".replace("ra", "**")) #Метод replace заменяет вхождения подстроки на заданную строку, по умолчанию — все
print("abracadabra".replace("ra", "**", 1))

translation_map = {ord("a"): "*", ord("b"): "?"}
print("abracadabra".translate(translation_map)) #Для множественной замены символов удобно использовать метод translate, который принимает словарь трансляции

#Есть куча предикатов, нужно читать в доке
print("100500".isdigit())
print("foo100500".isalnum())
print('foobar'.islower())


## Форматирование строк

print(str("я строка")) #str возвращает человекочитаемое представление объекта
print(repr("я строка")) #repr возвращает представление объекта, по которому можно однозначно восстановить его значение
print(ascii("я строка")) #ascii аналогичен repr по смыслу, но возвращаемая строка состоит только из символов ASCII

print("{}, {}, how are you?".format("Hello", "Sally"))
print("{!r}".format("я строка")) #: внутри {} можно опционально указать способ преобразования объекта в строку и спецификацию формата

print("{0}, {1}, {0}".format("hello", "kitty"))
print("{what}, {who}, {what}".format(what="hello", who="kitty"))

point = 0, 10
print("x = {0[0]}, y = {0[1]}".format(point))
point = {"x": 0, "y": 10}
print("x = {0[x]}, y = {0[y]}".format(point))


## Байты

print(b"\00\42\24\00")
chunk = "я строка".encode("utf-8")
print(chunk)
print(chunk.decode("utf-8"))
print(sys.getdefaultencoding())


## Файлы, ввод и вывод

# open("./HBA1.txt") # вариант открыть файл
#Аргументов у функции open довольно много, нас будут интересовать:
#	mode — определяет, в каком режиме будет открыт файл, возможные значения:
#		• "r", "w", "x", "a", "+",
#		• "b", "t".
#	для текстовых файлов можно также указать encoding и errors
# open("./admin.log", "a", encoding="cp1251", errors="ignore")
#Методы readline и readlines читают одну или все строчки соотвественно. 
#Можно указать максимальное количество символов, которые надо прочитать
#Метод write записывает строку в файл:
#>>> handle = open("./example.txt", "w")
#>>> handle.write("abracadabra")
#11 # количество записанных байт.
#Неявного добавления символа окончания строки при этом
#не происходит.
#• Записать последовательность строк можно с помощью
#метода writelines:
#>>> handle.writelines(["foo", "bar"])
#>>> handle.flush() - очищает буфер
#>>> handle.close() - закрывает файл и очищает буфер если там что-то было


## Стандартные потоки

#input("Name: ") #Для чтения sys.stdin используют функцию input

print("Hello, `sys.stdout`!", file=sys.stdout)
print("Hello, `sys.stderr`!", file=sys.stderr)
print(*range(4), sep="_")
print(*range(4), end="\n--\n")

#В модуле io реализована иерархия низкоуровневых классов для работы с вводом/выводом. 
#Полезные для обычных людей классы: io.StringIO и io.BytesIO.