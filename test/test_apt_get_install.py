import pytest
import subprocess
from apt_lib import check_installed
from apt_lib import cache_policy
from apt_lib import _install_package
from apt_lib import _purge_package

@pytest.mark.parametrize('define_keys', [()])
def test_install_one_pkg_without_keys(define_packages, install_package):
	for pkg in define_packages:
		assert check_installed(package=pkg)

@pytest.mark.parametrize('define_packages', [('braa', 'black')])
def test_install_several_pkgs(define_packages, install_package):
	for pkg in define_packages:
		assert check_installed(package=pkg)

@pytest.mark.parametrize('define_packages', [('braa-',)])
def test_install_with_hyphen(define_packages, install_package):
	for pkg in define_packages:
		assert not check_installed(package=pkg[:-1])

@pytest.mark.parametrize('define_packages', [('braa+',)])
def test_install_with_plus(define_packages, install_package):
	for pkg in define_packages:
		assert check_installed(package=pkg[:-1])

@pytest.mark.parametrize('define_packages', [('black-', 'braa+')])
def test_install_several_pkgs_with_hyphen_and_plus(define_packages, install_package):
	for pkg in define_packages:
		if pkg[-1] == '-':
			assert not check_installed(pkg[:-1])
		else:
			assert check_installed(pkg[:-1])

@pytest.mark.parametrize('define_packages', [('seccomp',)])
def test_install_with_choosing_version(define_packages):
	for pkg in define_packages:
		_purge_package(pkg)
		older_version = cache_policy(package=pkg)['older_version']
		candidate_version = cache_policy(package=pkg)['candidate_version']
		assert cache_policy(package=pkg)['installed_version'] == '(none)'
		package_with_version = f'{pkg}={older_version}'
		_install_package(package_with_version)
		assert cache_policy(package=pkg)['installed_version'] == older_version
		assert cache_policy(package=pkg)['installed_version'] != '(none)'
		assert cache_policy(package=pkg)['installed_version'] != candidate_version
		_purge_package(pkg)

def test_install_with_regular(clean, define_packages):
	for pkg in define_packages:
		output = subprocess.check_output(['ls', '/var/cache/apt/archives']).decode('utf-8')
		archive_len = len(output.strip().split('\n'))
		assert not check_installed(package=pkg, remove=True)
		subprocess.run(['sudo', 'apt-get', 'install', '-y', f'^{pkg}$'])
		assert check_installed(package=pkg)
		new_output = subprocess.check_output(['ls', '/var/cache/apt/archives']).decode('utf-8')
		new_archive_len = len(new_output.strip().split('\n'))
		assert new_archive_len == archive_len + 1
		_purge_package(pkg)

def test_install_quiet(define_packages):
	for pkg in define_packages:
		assert not check_installed(package=pkg, remove=True)
		quiet_cmd = ['sudo', 'apt-get', 'install', '-qq', '-y', pkg]
		quiet_output = subprocess.check_output(quiet_cmd).decode('utf-8')
		assert check_installed(package=pkg)
		_purge_package(pkg)
		cmd = ['sudo', 'apt-get', 'install', '-y', pkg]
		output = subprocess.check_output(cmd).decode('utf-8')
		assert len(quiet_output) < len(output)
		_purge_package(pkg)


@pytest.mark.parametrize('define_keys', [('-d',)])
def test_install_download_only(clean, define_packages, install_package):
	for pkg in define_packages:
		assert not check_installed(package=pkg)
		output = subprocess.check_output(['ls', '/var/cache/apt/archives']).decode('utf-8')
		assert pkg in output

def test_install_no_download(clean, define_packages):
	for pkg in define_packages:
		check_installed(package=pkg, remove=True)
		output = subprocess.check_output(['ls', '/var/cache/apt/archives']).decode('utf-8')
		assert pkg not in output
		with pytest.raises(subprocess.CalledProcessError):
			subprocess.check_output(['sudo','apt-get', 'install', '-y', '--no-download', pkg])
		subprocess.run(['sudo','apt-get', 'install', '-y', '-d', pkg])
		assert not check_installed(package=pkg)
		output = subprocess.check_output(['ls', '/var/cache/apt/archives']).decode('utf-8')
		assert pkg in output
		subprocess.run(['sudo','apt-get', 'install', '-y', '--no-download', pkg])
		assert check_installed(package=pkg)

def test_install_one_pkg_without_sudo(define_packages):
	for pkg in define_packages:
		check_installed(package=pkg, remove=True)
		with pytest.raises(subprocess.CalledProcessError):
			subprocess.check_output(['apt-get', 'install', '-y', pkg]).decode('utf-8')
		assert not check_installed(package=pkg)
		
@pytest.mark.parametrize('define_packages', [('braa', 'black')])
def test_install_wrong_package(clean, define_packages):
	wrong_package = ''.join(define_packages)
	for pkg in define_packages:
		check_installed(package=pkg, remove=True)
	_install_package(wrong_package)

