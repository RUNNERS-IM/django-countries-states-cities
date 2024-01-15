# filters.py

import django_filters
from countries_states_cities.models import Region, Subregion, Country, State, City


class FilterSetMixin(django_filters.FilterSet):
    ids = django_filters.CharFilter(method='filter_id')

    def filter_id(self, queryset, name, value):
        if value:
            ids = [int(id) for id in value.replace(' ', '').split(',') if id]
            return queryset.filter(id__in=ids)
        return queryset


class RegionFilter(FilterSetMixin):
    class Meta:
        model = Region
        fields = ['ids']


class SubregionFilter(FilterSetMixin):
    region = django_filters.NumberFilter(field_name='region_id')

    class Meta:
        model = Subregion
        fields = ['ids', 'region']


class CountryFilter(FilterSetMixin):
    region = django_filters.NumberFilter(field_name='region_id')

    class Meta:
        model = Country
        fields = ['ids', 'subregion']


class StateFilter(FilterSetMixin):
    region = django_filters.NumberFilter(field_name='region_id')

    class Meta:
        model = State
        fields = ['ids', 'region']


class CityFilter(FilterSetMixin):
    region = django_filters.NumberFilter(field_name='region_id')

    class Meta:
        model = City
        fields = ['ids', 'region']
