import math
import os
import csv
from decimal import Decimal

# Django
from django.db import migrations


def forwards_update(apps, schema_editor):
    Region = apps.get_model('countries_states_cities', 'Region')
    Subregion = apps.get_model('countries_states_cities', 'Subregion')
    Country = apps.get_model('countries_states_cities', 'Country')
    State = apps.get_model('countries_states_cities', 'State')
    City = apps.get_model('countries_states_cities', 'City')

    current_path = os.path.abspath(os.path.dirname(__file__))

    def csv_to_json(csvFilePath, model):
        jsonArray = []

        # read csv file
        with open(csvFilePath, encoding='utf-8') as csvf:
            # load csv file data using csv library's dictionary reader
            csvReader = csv.DictReader(csvf)

            # convert each csv row into python dict
            for row in csvReader:
                # add this python dict to json array
                row['id'] = int(row['id'])
                if 'region_id' in row:
                    try:
                        row['region'] = Region.objects.get(id=int(row['region_id']))
                    except:
                        row['region'] = None
                if 'subregion_id' in row:
                    try:
                        row['subregion'] = Subregion.objects.get(id=int(row['subregion_id']))
                    except:
                        row['subregion'] = None
                if 'country_id' in row:
                    try:
                        row['country'] = Country.objects.get(id=int(row['country_id']))
                    except:
                        row['country'] = None
                if 'state_id' in row:
                    try:
                        row['state'] = State.objects.get(id=int(row['state_id']))
                    except:
                        row['state'] = None

                if 'latitude' in row:
                    try:
                        row['latitude'] = Decimal(row['latitude'])
                    except:
                        row['latitude'] = None

                if 'longitude' in row:
                    try:
                        row['longitude'] = Decimal(row['longitude'])
                    except:
                        row['longitude'] = None
                jsonArray.append(model(**row))
                # print('[0002_import_csv] Read {} ({}%)'.format(index, math.floor((index + 1) / total * 100)))

        return jsonArray

    def csv_to_bulkdata(filenames, model):
        path = os.path.join(current_path, f'../../csv/{filenames}.csv')
        print('[0002_import_csv] Read the csv file located "{}" and convert it to Json'.format(path))
        return csv_to_json(path, model)

    def create_bulkdata(bulkdata):
        total = len(bulkdata)
        for index, data in enumerate(bulkdata):
            data.save()
            print('[0002_import_csv] Created {} ({}%)'.format(index, math.floor((index+1)/total*100)))

    Region.objects.bulk_create(csv_to_bulkdata('regions', Region))
    # create_bulkdata(csv_to_bulkdata('regions', Region))
    print('[0002_import_csv] Region creation is complete')

    Subregion.objects.bulk_create(csv_to_bulkdata('subregions', Subregion))
    # create_bulkdata(csv_to_bulkdata('subregions', Subregion))
    print('[0002_import_csv] Subregion creation is complete')

    Country.objects.bulk_create(csv_to_bulkdata('countries', Country))
    # create_bulkdata(csv_to_bulkdata('states', State))
    print('[0002_import_csv] Country creation is complete')

    # State.objects.bulk_create(csv_to_bulkdata('states', State))
    create_bulkdata(csv_to_bulkdata('states', State))
    print('[0002_import_csv] State creation is complete')

    # City.objects.bulk_create(csv_to_bulkdata('cities', City))
    create_bulkdata(csv_to_bulkdata('cities', City))
    print('[0002_import_csv] City creation is complete')


def reverse_update(apps, schema_editor):
    Region = apps.get_model('countries_states_cities', 'Region')
    Subregion = apps.get_model('countries_states_cities', 'Subregion')
    Country = apps.get_model('countries_states_cities', 'Country')
    State = apps.get_model('countries_states_cities', 'State')
    City = apps.get_model('countries_states_cities', 'City')

    City.objects.all().delete()
    State.objects.all().delete()
    Country.objects.all().delete()
    Subregion.objects.all().delete()
    Region.objects.all().delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('countries_states_cities', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_update,
            reverse_code=reverse_update,
        ),
    ]
