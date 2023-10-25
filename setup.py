import setuptools
import subprocess

version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

setuptools.setup(
    version=version,
    packages=setuptools.find_packages(include=['django_seeding']),
    install_requires=('django', 'djangorestframework', 'pandas'),
)
