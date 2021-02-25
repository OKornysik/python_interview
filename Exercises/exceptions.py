# ---------- Исключения ----------

# Исключения — это ошибки, которые можно обрабатывать
# BaseException — базовый класс для встроенных исключений в Python
print(BaseException.__subclasses__()) # ->  [<class 'Exception'>, <class 'GeneratorExit'>, <class 'KeyboardInterrupt'>, <class 'SystemExit'>]
# Напрямую от класса BaseException наследуются только системные исключения и исключения, приводящие к завершению работы интерпретатора
# Все остальные встроенные исключения, а также исключения, объявленные пользователем, должны наследоваться от класса Exception.

try:
	a = 1 + 5 # use 1 + 'dew' for geting exception
	print('im doing something')
except TypeError as e:
    print('I cought it!')
    raise e
else:
	print(f'there was no exception, a = {a}')
finally:
    print('closing program')

# Поднять исключение можно с помощью оператора raise
# Аргумент оператора raise должен наследоваться от базового класса BaseException
# Если вызвать оператор raise без аргумента, то он поднимет последнее пойманное исключение или, если такого исключения нет, RuntimeError

# AssertionError

def f(*args):
	assert all(i > 0 for i in args), 'args should be possitive'
	return sum(args)
	
print(f(1, 2, 7))

# Оператор assert используется для ошибок, которые могут возникнуть только в результате ошибки программиста,
# 	поэтому перехватывать AssertionError считается дурным тоном

# - Если оператор import не смог найти модуль с указанным именем, поднимается исключение ImportError
# 	NameError поднимается, если не была найдена локальная или глобальная переменная
# - Исключение AttributeError поднимается при попытке прочитать или (в случае __slots__) записать значение в
# 	несуществующий атрибут
# - Исключения KeyError и IndexError наследуются от базового класса LookupError и поднимаются, если в
# 	контейнере нет элемента по указанному ключу или индексу
# - Исключение ValueError используется в случаях, когда другие более информативные исключения, например,
# 	KeyError, не применимы
# - Исключение TypeError поднимается, когда оператор, функция или метод вызываются с аргументом
# 	несоответствующего типа

# Для объявления нового типа исключения достаточно объявить класс, наследующийся от базового класса Exception
# Хорошая практика при написании библиотек на Python — объявлять свой базовый класс исключений, например
class CSCException(Exception):
	pass
	
class TestFailure(CSCException):
	def __str__(self):
		return "lecture test failed"

# Наличие базового класса позволяет пользователю обработать любое исключение, специфичное для библиотеки в одной ветке except
try:
	print('data')
except CSCException:
	pass

# ---------- Менеджеры контекста  ----------

r = open('stt.txt')
try:
	_temp = [i for i in r]
	print(len(_temp))
finally:
	r.close()
	del _temp
# С помощью менеджера контекста пример выше можно записать так
with open('stt.txt') as r:
	_temp = [i for i in r]
	print(len(_temp))
	del _temp

import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print(f"Files in {cwd}: {files}")

with open('stt.txt') as p:
    _list = [i.strip() for i in p]
    print(_list)

# Протокол менеджеров контекста состоит из двух методов
# - Метод __enter__ инициализирует контекст, например, открывает файл или захватывает мьютекс. Значение,
# 	возвращаемое методом __enter__, записывается по имени, указанному после оператора as
# - Метод __exit__ вызывается после выполнения тела оператора with. Метод принимает три аргумента:
# 		1. тип исключения,
# 		2. само исключение и
# 		3. объект типа traceback.
# 	Если в процессе исполнения тела оператора with было поднятно исключение, метод __exit__ может подавить его, вернув True
# - Экземпляр любого класса, реализующего эти два метода, является менеджером контекста
# - Модуль tempfile реализует классы для работы с временными файлами

import os
class cd:
	def __init__(self, path):
		self.path = path

	def __enter__(self):
		self.saved_cwd = os.getcwd()
		os.chdir(self.path)

	def __exit__(self, *exc_info):
		os.chdir(self.saved_cwd)

print(os.getcwd()) # -> ./csc/python
with cd("/tmp"):
	print(os.getcwd()) # -> /tmp

# С помощью closing можно, например, безопасно работать с HTTP ресурсами
from contextlib import closing
from urllib.request import urlopen
url = "http://compscicenter.ru"
with closing(urlopen(url)) as page:
	print(len(page))

# Менеджер контекста redirect_stdout позволяет локально перехватывать вывод в стандартный поток
from contextlib import redirect_stdout
import io
handle = io.StringIO()
with redirect_stdout(handle):
	print("Hello, World!")
handle.getvalue() # -> 'Hello, World!\n'

# С помощью менеджера контекста suppress можно локального подавить исключения указанных типов:
from contextlib import suppress
with suppress(FileNotFoundError):
	os.remove("example.txt")
