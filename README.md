<!-- 
    Written By Suliman Awad
    Email: sulimanawadstudy@gmail.com
    Github: https://github.com/suliman-99
    Linkedin: https://linkedin.com/in/suliman-awad-399a471b8
    Facebook: https://www.facebook.com/suliman.awad.507
 -->
[![repo-size][repo-size-shield]][repo-url]
[![forks][forks-shield]][forks-url]
[![stars][stars-shield]][stars-url]
[![issues][issues-shield]][issues-url]
[![contributors][contributors-shield]][contributors-url]
[![pr][pr-shield]][contributing-url]
[![hachtoberfest][hachtoberfest-shield]][hacktoberfest-url]
[![license][license-shield]][license-url]


<div align="center">
<h3>Django Seeding</h3>

[Report Bug][issues-url]
    ·
[Request Feature][issues-url]

</div>

[![photo][photo-url]][demo-url]

***

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Contact](#contact)
- [License](#license)


## Introduction

This is a package that help developers seed thier database with real needed data instead of fil it manually


## Installation

Installing using pip:

```
pip install django-seeding:
```

add `'django_seeding'` to your `INSTALLED_APPS` setting:

```
INSTALLED_APPS = [
    ...
    'django_seeding',
]
```


## Usage

Let's take a look at a quick example of using django-seeding to build simples seeder to store it in the database.

django_seeding_example/models.py:
```
from django.db import models


class M1(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
```

django_seeding_example/seeders.py:
```
from django_seeding import seeders
from django_seeding.seeder_registry import SeederRegistry 
from django_seeding_example.models import M1

# this is a fast seeder on a model aith a csv file that contains the data
@SeederRegistry.register
class M1Seeder(seeders.CSVFileModelSeeder):
    id = 'M1Seeder'
    priopity = 1
    model = M1
    csv_file_path = 'django_seeding_example/seeders_data/M1Seeder.csv'
```

django_seeding_example/seeders_data/M1Seeder.csv:
```
title,description
t1,d1
t2,d2
```

then the seeder can be run by three ways:

* To seed with a specific command (Recommended):

```
python manage.py seed
```


* To seed with runserver manually just add "--seed" in runserver command:

```
python manage.py runserver --seed
```


* To seed on runserver automatically just set in your project settings:

``` 
SEEDING_ON_RUNSERVER = True
``` 

## Features

With django-seeding package you can:

* Use Full Implemenation for fast model seeding (bulk_create) by [ModelSeeder, CSVFileModelSeeder and JSONFileModelSeeder]
* Use Full Implemenation for slow serializer seeding one-by-one (not bulk_create) (to inject your logic in the seeder) by [SerializerSeeder, CSVFileSerializerSeeder and JSONFileSerializerSeeder]
* Use CSV file reader by pandas package
* Use JSON file reader
* write you custom seeder
* sort your seeders by the priority class-attribute
* give a specific identifiers to you seeder by id class-attribute
* limit a seeder to be applied just in the debug mode by just_debug class-attribute
* let the seeders be applied with the runserver with SEEDING_ON_RUNSERVER variable in you project settings file
* runserver with seeding with --seed (even that SEEDING_ON_RUNSERVER=False) : "python manage.py runserver --seed"
* runserver without seeding with --dont-seed (even that SEEDING_ON_RUNSERVER=True): "python manage.py runserver --dont-seed"


## Contributing

If you have suggestions for how Django Seeding could be improved, or want to report a bug, open an issue! We'd love all and any contributions.

For more, check out the [Contributing Guide][contributing-url].


## Contact

Suliman Awad - [sulimanawadstudy@gmail.com][gmail-url] - [Linkedin][linkedin-account-url]

Project Link: [https://github.com/suliman-99/django-seeding][repo-url]


## License

MIT License

Copyright (c) 2023 Suliman Awad

For more, check out the [License File][license-url].



<!-- ------------------------------------ urls ------------------------------------ -->


<!-- my urls -->
[gmail-url]: mailto:sulimanawadstudy@gmail.com
[linkedin-account-url]: https://linkedin.com/in/suliman-awad-399a471b8
[facebook-account-url]: https://www.facebook.com/suliman.awad.507
[codeforces-account-url]: https://codeforces.com/profile/Suliman_Awad
[github-account-url]: https://github.com/suliman-99


<!-- repo urls -->
[repo-url]: https://github.com/suliman-99/django-seeding
[contributors-url]: https://github.com/suliman-99/django-seeding/graphs/contributors
[forks-url]: https://github.com/suliman-99/django-seeding/network/members
[stars-url]: https://github.com/suliman-99/django-seeding/stargazers
[issues-url]: https://github.com/suliman-99/django-seeding/issues
[license-url]: ./LICENSE
[contributing-url]: ./CONTRIBUTING.md
[photo-url]: ./photo.png
[demo-url]: https://github.com/suliman-99/django-seeding


<!-- static urls -->
[hacktoberfest-url]: https://hacktoberfest.com
[python-url]: https://www.python.org
[python-downloads-url]: https://www.python.org/downloads
[django-url]: https://www.djangoproject.com
[mysql-url]: https://www.mysql.com
[postgresql-url]: https://www.postgresql.org
[restful-api-url]: https://aws.amazon.com/what-is/restful-api/?nc1=h_ls
[postman-url]: https://www.postman.com
[git-url]: https://git-scm.com
[git-downloads-url]: https://git-scm.com/downloads
[github-url]: https://github.com
[markdown-url]: https://en.wikipedia.org/wiki/Markdown
[vscode-url]: https://code.visualstudio.com



<!-- ------------------------------------ shields ------------------------------------ -->



<!-- my shields -->
[gmail-shield]: https://img.shields.io/badge/Gmail-sulimanawadstudy@gmail.com-blue?logo=gmail&style=flat-square
[linkedin-shield]: https://img.shields.io/badge/LinkedIn-Suliman%20Awad-blue?logo=linkedin&logoColor=6688ee&style=flat-square
[linkedin-shield2]: https://img.shields.io/badge/LinkedIn-black.svg?logo=linkedin&colorB=555&style=social
[facebook-shield]: https://img.shields.io/badge/Facebook-Suliman%20Awad-blue?logo=Facebook&style=flat-square

[codeforces-shield]: https://img.shields.io/badge/Suliman%20Awad-333333?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAQCAYAAAD0xERiAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAIOSURBVDhPpZHLa1NBFMa/O0naPG/E10Vb0pArunBha0C6cCVCVdwLImTnzoWIa1257J/h3+BGEN105053fRACai0Gkzbx3jt3POfMDEZss/GDjznz+s03M0G32zU4QZX4GrB6F35BeXsLw4/vXO9fKdcer9uPsXPqCnad97sP3MTxmgsr1UJXWU0yV5yg+cmMgcmddS7tPKmFhRJePFnH68075A28enoD9dqiTMpmb+YQfJ7Uxs027q0vIj5/iPjcGLeuF/Dw/mU76/d60Eyyi40Qa6fPiJfqDRlTzUaREiTklNangE5QK8ucAOz1yNpel9Wp1fF88B2PPm+Ln/W/4mo9pDczOZ1IMD2FyY6oOyWIlk0BQf5c05m0kmTIJxOpeUSnKaLRGMrQRqN/CZBoLiFB/EpOR7C/PoC51OjAGYGcJ8kEQLCcrihggsoegTDMgTxMIASgwoitLIwADJN0BOYxVs6p5HrU8TWPc9eZa9+feTObyl7TvlkmyfgwZ5dsFsIJ2ZxWGRpiACeSX9VHtNrC+Fr2Jx1oBuYhHgyq1c6AfpF+0P6iTdX/Zt8sOfhiV/IOcpnXkMaVMozAKL28H7XNJgrFSvQyKcXISssYjCJ8+BTizdYI1WoVZ9N9tFda6IQKy2qEC3tvUUwP8bNYQNBpo3IpxrTdQr+1hPc/DhD0ej0TRZGc+D8aDof4DQayYRrQETG1AAAAAElFTkSuQmCC&style=flat-square


<!-- repo shields -->
[repo-size-shield]: https://img.shields.io/github/repo-size/suliman-99/django-seeding.svg?label=Repo%20size&style=flat-square
[forks-shield]: https://img.shields.io/github/forks/suliman-99/django-seeding.svg?&style=flat-square
[stars-shield]: https://img.shields.io/github/stars/suliman-99/django-seeding.svg?&style=flat-square
[issues-shield]: https://img.shields.io/github/issues/suliman-99/django-seeding.svg?&style=flat-square
[contributors-shield]: https://img.shields.io/github/contributors/suliman-99/django-seeding.svg?&style=flat-square
[pr-shield]: https://img.shields.io/badge/PR-Welcome-333333?color=0055bb&style=flat-square
[hachtoberfest-shield]: https://img.shields.io/github/hacktoberfest/2022/suliman-99/django-seeding
[license-shield]: https://img.shields.io/github/license/suliman-99/django-seeding.svg?&style=flat-square

