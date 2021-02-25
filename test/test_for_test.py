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

def cache_policy(package=apt_lib.default_packages[0]):
	output = subprocess.check_output(['apt-cache', 'policy', package]).decode('utf-8')
	list_output = output.split('\n')
	_installed_version = list_output[1].strip().partition(' ')[-1]
	_candidate_version = list_output[2].strip().partition(' ')[-1]
	vers_and_reps = [v.strip().strip('*** ').partition(' ')[0] 
					for v in list_output[4:-1]]
	all_versions = [v for v in vers_and_reps 
					if not v.isdigit()]
	for ver in all_versions:
		if len(all_versions) > 1 and ver != _candidate_version:
			_older_version = ver
		else:
			_older_version = '(none)'
	return {'installed_version': _installed_version, 
			'candidate_version': _candidate_version, 
			'older_version': _older_version}


print(cache_policy(package='seccomp'))
pkg = 'black'
quiet_cmd = ['sudo', 'DEBIAN_FRONTEND=noninteractive', 'apt-get', 'install', '-qq', pkg]
a = subprocess.check_output(quiet_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).decode('utf-8')
print(a)