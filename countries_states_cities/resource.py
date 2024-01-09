# 3rd Party
from import_export import resources

# App
from countries_states_cities.models import Region, Subregion, Country, State, City
from countries_states_cities.utils import get_translated_fields


# Main Section
class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
        fields = ('id',) + get_translated_fields(Region, 'name')


class SubregionResource(resources.ModelResource):
    class Meta:
        model = Subregion
        fields = ('id',) + get_translated_fields(Subregion, 'name')


class CountryResource(resources.ModelResource):
    class Meta:
        model = Country
        fields = ('id',) + get_translated_fields(Country, 'name')


class StateResource(resources.ModelResource):
    class Meta:
        model = State
        fields = ('id',) + get_translated_fields(State, 'name')


class CityResource(resources.ModelResource):
    class Meta:
        model = City
        fields = ('id',) + get_translated_fields(City, 'name')
