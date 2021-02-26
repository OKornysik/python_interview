import pytest
import subprocess
from apt_lib import check_installed
from apt_lib import DEFAULTS


@pytest.fixture
def define_keys(request: object) -> tuple:
	try:
		return request.param
	except AttributeError:
		return DEFAULTS['default_keys']


@pytest.fixture
def define_packages(request: object) -> tuple:
	try:
		return request.param
	except AttributeError:
		return DEFAULTS['default_packages']


@pytest.fixture
def install_package(define_packages: tuple, define_keys: tuple) -> None:
	for pkg in define_packages:
		if pkg[-1] == '-' or '+':
			check_installed(package=pkg[:-1], remove=True)
		else:
			check_installed(package=pkg, remove=True)
	install_command = list(DEFAULTS['default_install_command'])
	install_command.extend(define_keys)
	install_command.extend(define_packages)
	print('Installing packages ', define_packages)
	install_text = subprocess.check_output(install_command).decode('utf-8')
	yield install_text
	for pkg in define_packages:
		if pkg[-1] == '-' or '+':
			check_installed(package=pkg[:-1], remove=True)
		else:
			check_installed(package=pkg, remove=True)


@pytest.fixture
def clean():
	subprocess.run(['apt-get', 'clean'])