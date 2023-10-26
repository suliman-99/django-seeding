import setuptools


setuptools.setup(
    packages=setuptools.find_packages(include=['django_seeding', 'django_seeding.*']),
    install_requires=('django', 'djangorestframework', 'pandas'),
)
