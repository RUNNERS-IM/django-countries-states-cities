from django.core.management.base import BaseCommand
import os
import csv
from decimal import Decimal
from django.db.models import Model
from django.db.models.fields.related import ForeignKey
from countries_states_cities.models import Region, Subregion, Country, State, City


class Command(BaseCommand):
    help = 'Imports data from CSV files into the specified models'
    current_path = os.path.abspath(os.path.dirname(__file__))

    def handle(self, *args, **options):
        models = [Region, Subregion, Country, State, City]
        for model in models:
            self.import_data_for_model(model)

    def import_data_for_model(self, model: Model):
        filename = self.get_plural_model_name(model.__name__).lower()
        csv_file_path = os.path.join(self.current_path, f'../../fixtures/csc_{filename}.csv')

        self.stdout.write(f'Starting import for {filename}...')  # 데이터 가져오기 시작 메시지

        with open(csv_file_path, mode='r', encoding='utf-8') as csvf:
            csv_reader = csv.DictReader(csvf)
            objects = []
            total_rows = sum(1 for _ in csv_reader)  # 전체 행의 수를 계산
            csvf.seek(0)  # 파일 포인터를 다시 처음으로 이동
            next(csv_reader)  # 헤더 행 건너뛰기

            for i, row in enumerate(csv_reader, 1):
                obj = self.process_row(row, model)
                if obj:
                    objects.append(obj)
                self.print_progress(i, total_rows, filename)

            model.objects.bulk_create(objects, ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'{filename.capitalize()} import completed'))

    def process_row(self, row, model: Model):
        for field in model._meta.get_fields():
            if field.name in row:
                if isinstance(field, ForeignKey):
                    row[field.name] = self.get_foreign_key_instance(field.related_model, row[field.name])
                elif field.get_internal_type() == 'DecimalField':
                    row[field.name] = Decimal(row[field.name]) if row[field.name] else None
        return model(**row)

    def get_foreign_key_instance(self, related_model, value):
        try:
            return related_model.objects.get(id=value) if value else None
        except related_model.DoesNotExist:
            return None

    def get_plural_model_name(self, model_name: str):
        plural_names = {
            'Region': 'regions',
            'Subregion': 'subregions',
            'Country': 'countries',
            'State': 'states',
            'City': 'cities'
        }
        return plural_names.get(model_name, model_name + 's')

    def print_progress(self, processed, total, model_name):
        progress = (processed / total) * 100
        self.stdout.write(f'Importing {model_name}: {processed}/{total} ({progress:.2f}%) complete')
