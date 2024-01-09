# django-countries-states-cities

## 1. Installation

The preferred installation method is directly from pypi:

```bash
# Create promgen setting directory.
$ pip install -U django-countries-states-cities
```

## 2. Quickstart

In ``settings.py``:
```python
INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    ...,
    'import_export',
    'countries_states_cities'
]

def gettext_noop(s):
    return s

LANGUAGES = [  # supported languages
    ("en", gettext_noop("English")),
    ("ja", gettext_noop("Japanese")),
    ("ko", gettext_noop("Korean")),
]
```

2. In ``urls.py``:
```python
from django.urls import path, include

urlpatterns = [
    ...,
    path('csc/', include('countries_states_cities.urls')),
]
```

3. Run ``python manage.py migrate``
Create the countries_states_cities models.
```bash
$ python manage.py migrate
```

## 3. Configuration
- Language setting: Todo

## 4. Importing Data

This package comes with two custom Django management commands to import data from CSV files and update translations. Follow the steps below to execute these commands:

### Importing Basic Data

1. Ensure your CSV files are placed in the correct directory (e.g., `./countries_states_cities/data/`).

2. Run the following command to import data from the CSV files into your Django models:
```bash
$ python manage.py import_csv
```
This command will import regions, subregions, countries, states, and cities data from the respective CSV files into the Django models.

3. Updating Translations
```bash
$ python manage.py import_translate_csv
```



## 5. Update Package

In ``setup.cfg``, upgrade version
```
[metadata]
name = django-countries-states-cities
version = x.x.x
...
```

Build package
```bash
$ python setup.py sdist bdist_wheel
```

Deploy package
```bash
$ twine upload --verbose dist/django-countries-states-cities-x.x.x.tar.gz
```

## The MIT License

Copyright (c) 2023 Runners Co.,Ltd.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.