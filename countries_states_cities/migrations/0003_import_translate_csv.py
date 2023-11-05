import math
import os
import csv

# Django
from django.db import migrations


def forwards_update(apps, schema_editor):
    Region = apps.get_model('countries_states_cities', 'Region')
    Subregion = apps.get_model('countries_states_cities', 'Subregion')
    Country = apps.get_model('countries_states_cities', 'Country')
    State = apps.get_model('countries_states_cities', 'State')
    City = apps.get_model('countries_states_cities', 'City')

    current_path = os.path.abspath(os.path.dirname(__file__))
    update_fields = ["name_en", "name_ko", "name_ja"]

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
                instance = model.objects.get(id=row['id'])

                for update_field in update_fields:
                    setattr(instance, update_field, row[update_field])
                jsonArray.append(instance)
                # print('[0003_import_translate_csv] Read {} ({}%)'.format(index, math.floor((index + 1) / total * 100)))

        return jsonArray

    def csv_to_bulkdata(filenames, model):
        path = os.path.join(current_path, f'../../csv/{filenames}_translated.csv')
        print('[0003_import_translate_csv] Read the csv file located "{}" and convert it to Json'.format(path))
        return csv_to_json(path, model)

    def update_bulkdata(bulkdata, update_fields):
        total = len(bulkdata)
        for index, data in enumerate(bulkdata):
            data.save(update_fields=update_fields)
            print('[0003_import_translate_csv] Translated {} ({}%)'.format(index, math.floor((index+1)/total*100)))

    Region.objects.bulk_update(csv_to_bulkdata('regions', Region), fields=update_fields)
    # update_bulkdata(csv_to_bulkdata('regions', Region))
    print('[0003_import_translate_csv] Region translation is complete')

    Subregion.objects.bulk_update(csv_to_bulkdata('subregions', Subregion), fields=update_fields)
    # update_bulkdata(csv_to_bulkdata('subregions', Subregion))
    print('[0003_import_translate_csv] Subregion translation is complete')

    Country.objects.bulk_update(csv_to_bulkdata('countries', Country), fields=update_fields)
    # update_bulkdata(csv_to_bulkdata('countries', Country))
    print('[0003_import_translate_csv] Country translation is complete')

    # State.objects.bulk_update(csv_to_bulkdata('states', State), fields=update_fields)
    update_bulkdata(csv_to_bulkdata('states', State), update_fields=update_fields)
    print('[0003_import_translate_csv] State translation is complete')

    # City.objects.bulk_update(csv_to_bulkdata('cities', City), fields=update_fields)
    update_bulkdata(csv_to_bulkdata('cities', City), update_fields=update_fields)
    print('[0003_import_translate_csv] City translation is complete')


def reverse_update(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('countries_states_cities', '0002_import_csv'),
    ]

    operations = [
        migrations.RunPython(
            code=forwards_update,
            reverse_code=reverse_update,
        ),
    ]
