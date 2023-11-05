from modeltranslation.translator import translator, TranslationOptions
from .models import Region, Subregion, Country, State, City


# Class Section
class BaseAreaTranslationOptions(TranslationOptions):
    fields = ('name',)


class RegionTranslationOptions(BaseAreaTranslationOptions):
    pass


class SubregionTranslationOptions(BaseAreaTranslationOptions):
    pass


class CountryTranslationOptions(BaseAreaTranslationOptions):
    pass


class StateTranslationOptions(BaseAreaTranslationOptions):
    pass


class CityTranslationOptions(BaseAreaTranslationOptions):
    pass


translator.register(Region, RegionTranslationOptions)
translator.register(Subregion, SubregionTranslationOptions)
translator.register(Country, CountryTranslationOptions)
translator.register(State, StateTranslationOptions)
translator.register(City, CityTranslationOptions)
