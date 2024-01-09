# vim: set fileencoding=utf-8 :
from django.contrib import admin, messages

# 3rd Party
from import_export.admin import ImportExportModelAdmin
from modeltranslation.admin import TranslationAdmin

# App
from countries_states_cities.models import Region, Subregion, Country, State, City
from countries_states_cities.utils import get_translated_fields
from countries_states_cities.resource import RegionResource, SubregionResource, CountryResource, StateResource, \
    CityResource


# Main Section
class BaseAreaAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    name_fields = get_translated_fields(Region, 'name')
    actions = ['translate_selected']
    inline_actions = ['translate']

    def get_list_display(self, request):
        return ('id',) + self.name_fields + self.list_display

    def get_search_fields(self, request):
        return self.name_fields + self.search_fields

    def translate(self, request, obj, parent_obj=None):
        try:
            obj.translate()
        except:
            print('[translate] Fail', obj)
            pass
        messages.success(request, '{obj} region have been successfully translated.'.format(obj=obj))

    def get_translate(self, obj):
        return 'Translate'

    def translate_selected(self, request, queryset=None):
        for obj in queryset:
            # try:
            obj.translate()
            # except:
            #     print('[translate] Fail', obj)
            #     pass
        messages.success(request, '{count} regions have been successfully translated.'.format(count=queryset.count()))

    translate_selected.short_description = '선택된 지역들 번역'


@admin.register(Region)
class RegionAdmin(BaseAreaAdmin, TranslationAdmin):
    resource_class = RegionResource


@admin.register(Subregion)
class SubregionAdmin(BaseAreaAdmin, TranslationAdmin):
    resource_class = SubregionResource


@admin.register(Country)
class CountryAdmin(BaseAreaAdmin, TranslationAdmin):

    list_display = (
        'region', 'subregion',
        'iso3', 'iso2', 'numeric_code', 'phone_code', 'capital',
        'currency', 'currency_name', 'currency_symbol',
        'tld', 'native', 'nationality',
        'latitude', 'longitude',
        'emoji', 'emojiU'
    )
    list_filter = ('region', 'subregion',)
    resource_class = CountryResource


@admin.register(State)
class StateAdmin(BaseAreaAdmin, TranslationAdmin):

    list_display = (
        'country', 'country_code', 'country_name',
        'state_code', 'type',
        'latitude', 'longitude',
    )
    list_filter = ('country',)
    resource_class = StateResource


@admin.register(City)
class CityAdmin(BaseAreaAdmin, TranslationAdmin):

    list_display = (
        'country', 'country_code', 'country_name',
        'state', 'state_code', 'state_name',
        'latitude', 'longitude',
        'wikiDataId',
    )
    list_filter = ('country', 'state',)
    resource_class = CityResource
