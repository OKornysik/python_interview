import pytest
import subprocess
from apt_lib import check_installed

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

def test_check_removed(define_packages):
	for pkg in define_packages:
		assert not check_installed(package=pkg)

@pytest.mark.parametrize('define_keys', [('-d',)])
def test_install_download_only(clean, define_packages, install_package):
	for pkg in define_packages:
		assert not check_installed(package=pkg)
		output = subprocess.check_output(['ls', '/var/cache/apt/archives']).decode('utf-8')
		assert pkg in output

#TODO --- Verify this
def test_install_no_download(clean, define_packages):
	for pkg in define_packages:
		with pytest.raises(subprocess.CalledProcessError):
			subprocess.check_output(['sudo','apt-get', 'install', '-y', '--no-download', pkg])
		assert not check_installed(package=pkg)
		output = subprocess.check_output(['ls', '/var/cache/apt/archives']).decode('utf-8')
		assert pkg not in output
		subprocess.run(['sudo','apt-get', 'install', '-y', '-d', pkg])
		assert not check_installed(package=pkg)
		output = subprocess.check_output(['ls', '/var/cache/apt/archives']).decode('utf-8')
		assert pkg in output
		subprocess.run(['sudo','apt-get', 'install', '-y', '--no-download', pkg])
		assert check_installed(package=pkg)
