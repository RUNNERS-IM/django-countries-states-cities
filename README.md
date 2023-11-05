# GoCardless sample application


Install using pip:

```sh
$ pip install django-countries-states-cities
```

Then add 'countries_states_cities' to your INSTALLED_APPS.

```python
INSTALLED_APPS = [
    ...
    'countries_states_cities',
]
```

## Usage

setting.py
```python
def gettext_noop(s):
    return s

LANGUAGES = [  # supported languages
    ("en", gettext_noop("English")),
    ("ja", gettext_noop("Japanese")),
    ("ko", gettext_noop("Korean")),
]
```

urls.py
```python

urlpatterns = [
    path('admin/', admin.site.urls),
    path('csc/', include('countries_states_cities.urls')),
]
```
