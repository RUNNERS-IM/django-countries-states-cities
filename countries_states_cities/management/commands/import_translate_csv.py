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
        filename = self.get_plural_model_name(model.__name__).lower()  # 모델명을 복수형으로 변환
        data = self.csv_to_bulkdata(filename, model)
        self.update_bulkdata(data, model)
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

    def get_plural_model_name(self, model_name):  # 이전 커맨드에서 사용한 동일한 메소드
        plural_names = {
            'Region': 'regions',
            'Subregion': 'subregions',
            'Country': 'countries',
            'State': 'states',
            'City': 'cities'
        }
        return plural_names.get(model_name, model_name + 's')

    def csv_to_bulkdata(self, filename, model):
        path = os.path.join(self.current_path, f'../data/csv/{filename}_translated.csv')
        self.stdout.write(f'Reading CSV file at "{path}" for {model.__name__}')
        return self.csv_to_json(path, model)

    def update_bulkdata(self, bulkdata, model):
        total = len(bulkdata)
        for index, data in enumerate(bulkdata):
            data.save(update_fields=self.update_fields)  # update_fields 파라미터 제공
            progress = (index + 1) / total * 100
            self.stdout.write(f'Updating {model.__name__}: {index + 1}/{total} ({progress:.2f}%) complete')
