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
urlpatterns = [
    ...,
    path('csc/', include('countries_states_cities.urls')),
]
```

3. Run ``python manage.py migrate``
Create the countries_states_cities models.
```python
$ python manage.py migrate
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