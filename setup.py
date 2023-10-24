import setuptools
from pathlib import Path


setuptools.setup(
    name='django-seeding',
    version='1.0.6',
    description='Simple Django Package that helps developer to seed data from files and codes into the database automatically',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=['django_seeding']),
    install_requires=('django', 'djangorestframework', 'pandas')
)
