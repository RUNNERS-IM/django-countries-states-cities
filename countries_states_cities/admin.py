# vim: set fileencoding=utf-8 :
from django.contrib import admin, messages

# 3rd Party
from modeltranslation.admin import TranslationAdmin

# App
import countries_states_cities.models as models


# Main Section

class BaseAreaAdmin(admin.ModelAdmin):

    actions = ['translate_selected']
    inline_actions = ['translate']

    def get_list_display(self, request):
        return ('id', 'name',) + self.list_display

    def get_search_fields(self, request):
        return ('name',) + self.search_fields

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


class RegionAdmin(BaseAreaAdmin, TranslationAdmin):
    pass


class SubregionAdmin(BaseAreaAdmin, TranslationAdmin):
    pass


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


class StateAdmin(BaseAreaAdmin, TranslationAdmin):

    list_display = (
        'country', 'country_code', 'country_name',
        'state_code', 'type',
        'latitude', 'longitude',
    )
    list_filter = ('country',)


class CityAdmin(BaseAreaAdmin, TranslationAdmin):

    list_display = (
        'country', 'country_code', 'country_name',
        'state', 'state_code', 'state_name',
        'latitude', 'longitude',
        'wikiDataId',
    )
    list_filter = ('country', 'state',)


def _register(model, admin_class):
    admin.site.register(model, admin_class)


_register(models.Region, RegionAdmin)
_register(models.Subregion, SubregionAdmin)
_register(models.Country, CountryAdmin)
_register(models.State, StateAdmin)
_register(models.City, CityAdmin)
