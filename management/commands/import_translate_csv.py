# managemant/commands/import_translate_csv.py
from django.core.management.base import BaseCommand
import os
import csv

from countries_states_cities.models import Region, Subregion, Country, State, City


class Command(BaseCommand):
    help = 'Updates translation data from CSV files into the specified models'
    current_path = os.path.abspath(os.path.dirname(__file__))
    update_fields = ["name_en", "name_ko", "name_ja"]

    def handle(self, *args, **options):
        models = [Region, Subregion, Country, State, City]
        for model in models:
            self.update_translations_for_model(model)
        self.stdout.write(self.style.SUCCESS('All translations successfully updated!'))

    def update_translations_for_model(self, model):
        filename = model.__name__.lower()
        data = self.csv_to_bulkdata(filename, model)
        self.update_bulkdata(data, model, self.update_fields)
        self.stdout.write(self.style.SUCCESS(f'{filename.capitalize()} translation completed'))

    def csv_to_json(self, csvFilePath, model):
        jsonArray = []
        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for row in csvReader:
                try:
                    instance = self.get_instance(row, model)
                    self.update_instance(instance, row)
                    jsonArray.append(instance)
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error updating row {row}: {e}'))
        return jsonArray

    def get_instance(self, row, model):
        row['id'] = int(row['id'])
        return model.objects.get(id=row['id'])

    def update_instance(self, instance, row):
        for update_field in self.update_fields:
            setattr(instance, update_field, row[update_field])

    def csv_to_bulkdata(self, filenames, model):
        path = os.path.join(self.current_path, f'../data/{filenames}_translated.csv')
        self.stdout.write(f'Reading CSV file at "{path}" for {model.__name__}')
        return self.csv_to_json(path, model)

    def update_bulkdata(self, bulkdata, model, update_fields):
        total = len(bulkdata)
        for index, data in enumerate(bulkdata):
            data.save(update_fields=update_fields)
            progress = (index + 1) / total * 100
            self.stdout.write(f'Updating {model.__name__}: {index + 1}/{total} ({progress:.2f}%) complete')
