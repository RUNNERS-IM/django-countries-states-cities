# django-countries-states-cities

## 1. Installation

The preferred installation method is directly from pypi:

```bash
# Install django-countries-states-cities
$ pip install -U django-countries-states-cities
```
This Django library is built using the [Countries States Cities Database](https://github.com/dr5hn/countries-states-cities-database).

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

LANGUAGES = [
    ("en", "English"),
    ("ko", "Korean"),
    ("ja", "Japanese"),
    ('zh-hans', 'Simplified Chinese'),  # 간체 중국어
    ('zh-hant', 'Traditional Chinese'),  # 번체 중국어
    ("es", "Spanish"),
    ("ru", "Russian"),
    ("ar", "Arabic"),
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

## 3. Database Setup
Run the following commands to set up the database:

```bash
# Create migration files for countries_states_cities models
$ python manage.py makemigrations countries_states_cities

# Apply migrations to create countries_states_cities models
$ python manage.py migrate
```

## 4. Loading Initial Data
To load initial data into the database, run the custom command:
```bash
$ python manage.py csc_loaddata_csv
```
This command will import data from predefined CSV files into the database.

## 5. Further Configuration
For further configuration and usage instructions, please refer to the official documentation.

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