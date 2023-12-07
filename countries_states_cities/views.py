# Python
from decimal import Decimal

# Django
from django.db.models.expressions import RawSQL
from django.utils.encoding import force_str

# Django Rest Framework
from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.compat import coreapi, coreschema, distinct

# Third Party
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

# Django Gis
# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.measure import D
# from django.contrib.gis.geos import Point

# countries_states_cities
from countries_states_cities.models import Region, Subregion, Country, State, City
from countries_states_cities.serializers import RegionSerializer, SubregionSerializer, CountrySerializer, StateSerializer, CitySerializer


# Variable Section
name_search_fields = ['name', 'name_en', 'name_ja', 'name_ko']


# Class Section
def sort_by_nearest(queryset, latitude: Decimal, longitude: Decimal, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    # Great circle distance formula
    gcd_formula = "6371 * acos(least(greatest(\
    cos(radians(%s)) * cos(radians(latitude)) \
    * cos(radians(longitude) - radians(%s)) + \
    sin(radians(%s)) * sin(radians(latitude)) \
    , -1), 1))"
    distance_raw_sql = RawSQL(gcd_formula, (latitude, longitude, latitude))

    latitude_diff = 1
    longitude_diff = 1
    qs = queryset.filter(
        latitude__range=[Decimal(latitude - latitude_diff), Decimal(latitude + latitude_diff)],
        longitude__range=[Decimal(longitude - longitude_diff), Decimal(longitude + longitude_diff)],
    ).annotate(distance=distance_raw_sql).order_by('distance')

    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance)
    return qs


class DistanceOrdering(OrderingFilter):
    ordering_latitude_param = 'latitude'
    ordering_latitude_description = 'Latitude to sort.'
    ordering_longitude_param = 'longitude'
    ordering_longitude_description = 'Longitude to sort.'

    ordering_fields = ['location']

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)

        if not ordering:
            # implement a custom ordering here
            ordering = ['-id']

        if 'location' in ordering:
            try:
                latitude = request.query_params.get(self.ordering_latitude_param)
                longitude = request.query_params.get(self.ordering_longitude_param)
                latitude = Decimal(latitude)
                longitude = Decimal(longitude)
                return sort_by_nearest(queryset, latitude, longitude)
            except:
                pass

        if ordering:
            return queryset.order_by(*ordering)

        return queryset

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.ordering_title),
                    description=force_str(self.ordering_description)
                )
            ),
            coreapi.Field(
                name=self.ordering_latitude_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.ordering_latitude_param),
                    description=force_str(self.ordering_latitude_description)
                )
            ),
            coreapi.Field(
                name=self.ordering_longitude_param,
                required=False,
                location='query',
                schema=coreschema.String(
                    title=force_str(self.ordering_longitude_param),
                    description=force_str(self.ordering_longitude_description)
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': self.ordering_param,
                'required': False,
                'in': 'query',
                'description': force_str(self.ordering_description),
                'schema': {
                    'type': 'string',
                },
            }, {
                'name': self.ordering_latitude_param,
                'required': False,
                'in': 'query',
                'description': force_str(self.ordering_latitude_description),
                'schema': {
                    'type': 'string',
                },
            }, {
                'name': self.ordering_longitude_param,
                'required': False,
                'in': 'query',
                'description': force_str(self.ordering_longitude_description),
                'schema': {
                    'type': 'string',
                },
            },
        ]


class IdsFilterSet(django_filters.FilterSet):
    ids = django_filters.CharFilter(method='filter_id')

    def filter_id(self, queryset, name, value):
        if value:
            ids = [int(id) for id in value.replace(' ', '').split(',') if id]
            print(ids)
            queryset = queryset.filter(id__in=ids)

        return queryset


class ViewSetMixin(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    search_fields = name_search_fields
    filter_backends = [DistanceOrdering, filters.SearchFilter, DjangoFilterBackend]
    filterset_class = IdsFilterSet


class RegionViewSet(ViewSetMixin):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = ViewSetMixin.filter_backends


class SubregionViewSet(ViewSetMixin):
    queryset = Subregion.objects.all()
    serializer_class = SubregionSerializer
    filterset_fields = ['ids', 'region']


class CountryViewSet(ViewSetMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_fields = ['ids', 'subregion']


class StateViewSet(ViewSetMixin):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filterset_fields = ['ids', 'country']


class CityViewSet(ViewSetMixin):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_fields = ['ids', 'country', 'state']
