# Django
from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

# 3rd Party
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin
from concurrent.futures import ThreadPoolExecutor, as_completed

# App
from countries_states_cities.models import Region, Subregion, Country, State, City
from countries_states_cities.utils import get_translated_fields
from countries_states_cities.resource import RegionResource, SubregionResource, CountryResource, StateResource, \
    CityResource


# Main Section
class BaseAreaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    actions = ['mark_duplicates_as_duplicated', 'update_wikidata_id', 'translate_selected']
    list_filter = ('is_duplicated',)
    list_editable = ('wikiDataId',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name_fields = self.get_translated_fields('name')
        self.list_display = ('id',) + self.name_fields + ('wikidata_link', 'wikiDataId', 'is_duplicated', 'updated_at')

    # Options
    def get_search_fields(self, request):
        return self.name_fields + self.search_fields + ('id', 'wikiDataId')

    def get_translated_fields(self, field_name):
        return get_translated_fields(self.model, field_name)

    # Fields
    def wikidata_link(self, obj):
        if obj.wikiDataId:
            url = f"https://www.wikidata.org/wiki/{obj.wikiDataId}"
            return format_html('<a href="{}" target="_blank">{}</a>', url, obj.wikiDataId)
        return '-'
    wikidata_link.short_description = 'WikiData ID'

    # Actions
    def mark_duplicates_as_duplicated(self, request, queryset):
        # 중복된 wikiDataId를 가진 객체들의 ID를 찾습니다.
        duplicates_wikiDataIds = self.model.objects.find_duplicates()
        print("Found duplicates:", duplicates_wikiDataIds)

        # queryset에서 중복된 wikiDataId를 가진 객체들을 찾습니다.
        to_update_true = queryset.filter(wikiDataId__in=duplicates_wikiDataIds)
        # 모든 중복 객체들의 is_duplicated 필드를 True로 설정합니다.
        for obj in to_update_true:
            obj.is_duplicated = True
            print(f'Marking {obj} as duplicated')

        # 대량 업데이트를 수행합니다.
        self.model.objects.bulk_update(to_update_true, ['is_duplicated'])
        print(f'Marked {to_update_true.count()} items as duplicated')

        # 중복되지 않은 항목들을 찾아 is_duplicated 필드를 False로 설정합니다.
        to_update_false = queryset.exclude(wikiDataId__in=duplicates_wikiDataIds)
        for obj in to_update_false:
            obj.is_duplicated = False
            print(f'Marking {obj} as not duplicated')

        # 대량 업데이트를 수행합니다.
        self.model.objects.bulk_update(to_update_false, ['is_duplicated'])
        print(f'Marked {to_update_false.count()} items as not duplicated')

        messages.success(request, f'{to_update_true.count()} items marked as duplicated, '
                                  f'{to_update_false.count()} items marked as not duplicated.')

    def translate_selected(self, request, queryset):
        queryset = queryset.filter(wikiDataId__isnull=False, translations__isnull=True)
        total = len(queryset)
        translated_count = 0
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_obj = {executor.submit(obj.translate): obj for obj in queryset}
            for future in as_completed(future_to_obj):
                obj = future_to_obj[future]
                try:
                    future.result()
                    translated_count += 1
                    print(f"Translation Progress: {translated_count}/{total} ({(translated_count / total) * 100:.2f}%)")
                except Exception as e:
                    messages.error(request, f'Failed to translate {obj}: {e}')

        messages.success(request, f'{translated_count}/{total} items have been successfully translated.')

    translate_selected.short_description = _('Translate selected items')

    def update_wikidata_id(self, request, queryset):
        total = len(queryset)
        updated_count = 0
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_obj = {executor.submit(obj.update_wikidata_id): obj for obj in queryset}
            for future in as_completed(future_to_obj):
                obj = future_to_obj[future]
                try:
                    future.result()
                    updated_count += 1
                    print(
                        f"Wikidata ID Update Progress: {updated_count}/{total} ({(updated_count / total) * 100:.2f}%)")
                except Exception as e:
                    messages.error(request, f'Failed to update wikidata ID for {obj}: {e}')

        messages.success(request, f'{updated_count}/{total} items have been successfully updated.')

    update_wikidata_id.short_description = _('Update Wikidata ID')


@admin.register(Region)
class RegionAdmin(BaseAreaAdmin, TranslationAdmin):
    list_display = BaseAreaAdmin.list_display
    resource_class = RegionResource


@admin.register(Subregion)
class SubregionAdmin(BaseAreaAdmin, TranslationAdmin):
    list_display = BaseAreaAdmin.list_display + ('region',)
    resource_class = SubregionResource


@admin.register(Country)
class CountryAdmin(BaseAreaAdmin, TranslationAdmin):

    list_display = BaseAreaAdmin.list_display + ('region', 'subregion')
    list_filter = BaseAreaAdmin.list_filter + ('region', 'subregion',)
    resource_class = CountryResource


@admin.register(State)
class StateAdmin(BaseAreaAdmin, TranslationAdmin):

    list_display = BaseAreaAdmin.list_display + ('country',)
    list_filter = BaseAreaAdmin.list_filter + ('country',)
    resource_class = StateResource

    actions = BaseAreaAdmin.actions + ['update_wikidata_and_translations']


@admin.register(City)
class CityAdmin(BaseAreaAdmin, TranslationAdmin):

    list_display = BaseAreaAdmin.list_display + ('country', 'state')
    list_filter = BaseAreaAdmin.list_filter + ('country', 'state',)
    resource_class = CityResource
