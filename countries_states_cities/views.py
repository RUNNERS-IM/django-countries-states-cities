from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from countries_states_cities.models import Region, Subregion, Country, State, City
from countries_states_cities.serializers import RegionSerializer, SubregionSerializer, CountrySerializer, StateSerializer, CitySerializer


name_search_fields = ['name', 'name_en', 'name_ja', 'name_ko']


class ViewSetMixin(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    search_fields = name_search_fields
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]


class RegionViewSet(ViewSetMixin):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class SubregionViewSet(ViewSetMixin):
    queryset = Subregion.objects.all()
    serializer_class = SubregionSerializer
    filterset_fields = ['region',]


class CountryViewSet(ViewSetMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_fields = ['region', 'subregion']


class StateViewSet(ViewSetMixin):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filterset_fields = ['country',]


class CityViewSet(ViewSetMixin):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_fields = ['country', 'state',]
