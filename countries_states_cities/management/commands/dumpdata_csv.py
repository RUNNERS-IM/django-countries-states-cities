from django.conf import settings
from django.core.management.base import BaseCommand
import os
import csv
from django.db.models.fields.related import ForeignKey
from countries_states_cities.models import Region, Subregion, Country, State, City


class Command(BaseCommand):
    help = 'Exports non-translation fields data to CSV files for specific models'
    current_path = os.path.abspath(os.path.dirname(__file__))

    def handle(self, *args, **options):
        models = [Region, Subregion, Country, State, City]
        for model in models:
            self.export_model_to_csv(model)
        self.stdout.write(self.style.SUCCESS('Selected models data successfully exported!'))

    def export_model_to_csv(self, model):
        plural_model_name = self.get_plural_model_name(model.__name__)
        csv_file_path = os.path.join(self.current_path, f'../../fixtures/csc_{plural_model_name}.csv')
        self.stdout.write(f'Exporting data to CSV file at "{csv_file_path}" for {plural_model_name}')

        total_records = model.objects.count()
        processed_records = 0

        with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csvf:
            field_names = self.get_field_names(model)
            csv_writer = csv.DictWriter(csvf, fieldnames=field_names)
            csv_writer.writeheader()

            for instance in model.objects.all():
                csv_writer.writerow({field: self.get_field_value(instance, field) for field in field_names})
                processed_records += 1
                self.print_progress(processed_records, total_records, plural_model_name)

    def get_field_names(self, model):
        # 모든 필드를 포함하되, 제외할 필드는 빼고 포함
        excluded_fields = ['created_at', 'updated_at']
        return [field.name for field in model._meta.fields if field.name not in excluded_fields]

    def get_field_value(self, instance, field_name):
        field = instance._meta.get_field(field_name)
        if isinstance(field, ForeignKey):
            return getattr(instance, f"{field_name}_id", None)
        return getattr(instance, field_name, None)

    def is_translation_field(self, field_name):
        language_codes = [code for code, _ in settings.LANGUAGES]
        complex_language_codes = ['zh_hans', 'zh_hant']  # 복합 언어 코드 추가

        for lang_code in language_codes + complex_language_codes:
            if field_name.endswith(f'_{lang_code}'):
                return True

        return False

    def get_plural_model_name(self, model_name):
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
        self.stdout.write(f'Processed {processed}/{total} records for {model_name} ({progress:.2f}%)')
