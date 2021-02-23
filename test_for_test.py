import pytest
import subprocess
import sys
#from apt_lib import check_installed
import apt_lib

@pytest.fixture
def define_keys(request: object) -> object:
	try:
		return request.param
	except AttributeError:
		return default_keys

@pytest.fixture
def define_packages(request: object) -> object:
	try:
		return request.param
	except AttributeError:
		return default_packages

@pytest.fixture
def install(define_keys: tuple, define_packages: tuple):
	install_command = list(default_install_command)
	install_command.extend(define_keys)
	install_command.extend(define_packages)
	return install_command
	
@pytest.mark.parametrize('define_keys, define_packages', 
						[(('-y', '-d'), ('braa', ))], indirect=['define_packages'])
def test_1(install):
	assert install == 'kaka'

apt_lib.check_installed(package='black')