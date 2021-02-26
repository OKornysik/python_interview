import pytest
import subprocess


DEFAULTS = {
    'default_packages': ('black',),
    'default_keys': (),
    'default_install_command': ('apt-get', 'install', '-y'),
    'default_purge_command': ('apt-get', 'purge', '-y')
}


def _install_package(package, keys=None):
	command = list(DEFAULTS['default_install_command'])
	if keys:
		command.extend(keys)
	command.append(package)
	subprocess.run([c for c in command])


def _purge_package(package, keys=None):
	command = list(DEFAULTS['default_purge_command'])
	if keys:
		command.extend(keys)
	command.append(package)
	subprocess.run([c for c in command])


def check_installed(package=DEFAULTS['default_packages'][0],
                    remove=False, install=False):
    status = False
    try:
        output = subprocess.check_output([package, '-h']).decode('utf-8')
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


def cache_policy(package=DEFAULTS['default_packages'][0]):
    output = subprocess.check_output(
        ['apt-cache', 'policy', package]).decode('utf-8')
    list_output = output.split('\n')
    _installed_version = list_output[1].strip().partition(' ')[-1]
    _candidate_version = list_output[2].strip().partition(' ')[-1]
    vers_and_reps = [v.strip().strip('*** ').partition(' ')[0]
                     for v in list_output[4:-1]]
    all_versions = [v for v in vers_and_reps if not v.isdigit()]
    for ver in all_versions:
        if len(all_versions) > 1 and ver != _candidate_version:
            _older_version = ver
        else:
            _older_version = '(none)'
    versions_dict = {
        'installed_version': _installed_version,
        'candidate_version': _candidate_version,
        'older_version': _older_version
    }
    return versions_dict