# django-countries-states-cities

## 1. Database Setup
Run the following commands to set up the database:

```bash
# Create migration files for countries_states_cities models
$ python manage.py makemigrations

# Apply migrations to create countries_states_cities models
$ python manage.py migrate
```

## 2. Data Management


### CSV Format

#### Exporting Data to CSV

Export the data from the Django models to CSV format. This can be useful for data analysis or sharing with systems that require CSV format.

```bash
$ python manage.py dumpdata_csv
```

#### Importing Data from CSV

Load data into the Django models from CSV files. This is useful when integrating data from external sources that provide CSV files.

```bash
$ python manage.py loaddata_csv
```


### JSON Format

#### Exporting Data to JSON

Export the data from the Django models to JSON format. This is useful for backing up data or transferring data between systems.

```bash
$ python manage.py dumpdata countries_states_cities.Region --output countries_states_cities/fixtures/csc_regions.json --indent 2
$ python manage.py dumpdata countries_states_cities.Subregion --output countries_states_cities/fixtures/csc_subregions.json --indent 2
$ python manage.py dumpdata countries_states_cities.Country --output countries_states_cities/fixtures/csc_countries.json --indent 2
$ python manage.py dumpdata countries_states_cities.State --output countries_states_cities/fixtures/csc_states.json --indent 2
$ python manage.py dumpdata countries_states_cities.City --output countries_states_cities/fixtures/csc_cities.json --indent 2
```

#### Importing Data from JSON

Load data into the Django models from JSON files. This is typically done after initially setting up the database or when restoring from a backup.

```bash
$ python manage.py loaddata csc_regions.json
$ python manage.py loaddata csc_subregions.json
$ python manage.py loaddata csc_countries.json
$ python manage.py loaddata csc_states.json
$ python manage.py loaddata csc_cities.json
```


## 3. Package Maintenance

### Versioning

Before releasing a new version of the package, update the version number in setup.cfg.

```
[metadata]
name = django-countries-states-cities
version = x.x.x
...
```

### Building the Package

Build the package into distribution formats.

```bash
$ python setup.py sdist bdist_wheel
```

### Publishing the Package

Upload the built package to PyPI.

```bash
$ twine upload --verbose dist/django-countries-states-cities-x.x.x.tar.gz
```

Remember to tag the release in your version control system and create a new release on the project's GitHub page.
