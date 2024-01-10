# managemant/commands/import_csv.py
from django.core.management.base import BaseCommand
import os
import csv
from decimal import Decimal

from countries_states_cities.models import Region, Subregion, Country, State, City


class Command(BaseCommand):
    help = 'Imports data from CSV files into the specified models'
    current_path = os.path.abspath(os.path.dirname(__file__))

    def handle(self, *args, **options):
        models = [Region, Subregion, Country, State, City]
        for model in models:
            self.import_data_for_model(model)
        self.stdout.write(self.style.SUCCESS('All data successfully imported!'))

    def import_data_for_model(self, model):
        filename = self.get_plural_model_name(model.__name__)  # model.__name__을 사용
        data = self.csv_to_bulkdata(filename, model)
        self.create_bulkdata(data, filename)
        self.stdout.write(self.style.SUCCESS(f'{filename.capitalize()} creation completed'))

    def csv_to_json(self, csvFilePath, model):
        jsonArray = []
        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for row in csvReader:
                # try:
                self.process_row(row, model)
                jsonArray.append(model(**row))
                # except Exception as e:
                #     self.stdout.write(self.style.ERROR(f'Error processing row {row}: {e}'))
        return jsonArray

    def process_row(self, row, model):
        row['id'] = int(row['id'])
        self.assign_foreign_key(row, 'region_id', Region)
        self.assign_foreign_key(row, 'subregion_id', Subregion)
        self.assign_foreign_key(row, 'country_id', Country)
        self.assign_foreign_key(row, 'state_id', State)
        self.convert_to_decimal(row, 'latitude')
        self.convert_to_decimal(row, 'longitude')

    def assign_foreign_key(self, row, field_name, model):
        if field_name in row:
            try:
                row[field_name[:-3]] = model.objects.get(id=int(row[field_name]))
            except:
                row[field_name[:-3]] = None

    def convert_to_decimal(self, row, field_name):
        if field_name in row:
            try:
                row[field_name] = Decimal(row[field_name])
            except:
                row[field_name] = None

    def get_plural_model_name(self, model_name):  # self 매개변수 추가
        plural_names = {
            'Region': 'regions',
            'Subregion': 'subregions',
            'Country': 'countries',
            'State': 'states',
            'City': 'cities'
        }
        return plural_names.get(model_name, model_name + 's')

    def csv_to_bulkdata(self, filename, model):  # plural_filename 대신 filename 사용
        path = os.path.join(self.current_path, f'../data/csv/{filename}.csv')
        self.stdout.write(f'Reading CSV file at "{path}" for {model.__name__}')
        return self.csv_to_json(path, model)

    def create_bulkdata(self, bulkdata, model_name):
        total = len(bulkdata)
        for index, data in enumerate(bulkdata):
            data.save()
            progress = (index + 1) / total * 100
            self.stdout.write(f'Importing {model_name}: {index + 1}/{total} ({progress:.2f}%) complete')
