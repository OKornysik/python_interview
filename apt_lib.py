import pytest
import subprocess

default_packages = ('black',)
default_keys = ()
default_install_command = ('sudo','apt-get', 'install', '-y')
default_purge_command = ('sudo','apt-get', 'purge', '-y')

def _install_package(package, keys=None):
	command = list(default_install_command)
	if keys:
		command.extend(keys)
	command.append(package)
	print(command, package)
	out_text = subprocess.check_output([c for c in command]).decode('utf-8')
	print(out_text)

def _purge_package(package, keys=None):
	command = list(default_purge_command)
	if keys:
		command.extend(keys)
	command.append(package)
	print(command, package)
	out_text = subprocess.check_output([c for c in command]).decode('utf-8')
	print(out_text)

def check_installed(package=default_packages[0], remove=False, install=False):
	status = False
	try:
		output = subprocess.check_output([package,'-h']).decode('utf-8')
	except OSError:
		status = False
		print(package, ' is not installed')
		if install:
			print('Installing ', package, ' ...')
			_install_package(package)
			status = True
			print(package, ' is installed')
	else:
		status = True
		print(package, ' is installed')
		if remove:
			print('Removing ', package, ' ...')
			_purge_package(package)
			status = False
			print(package, ' is not installed')
	finally:
		return status

