# views.py

# Python
from decimal import Decimal

# Django
from django.db.models import Func
from django.db.models.expressions import RawSQL
from django.utils.encoding import force_str
from django.utils.translation import get_language

# Django Rest Framework
from rest_framework import mixins, filters
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.compat import coreapi, coreschema

# Third Party
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

# Django Gis
# from django.contrib.gis.db.models.functions import Distance
# from django.contrib.gis.measure import D
# from django.contrib.gis.geos import Point

# countries_states_cities
from countries_states_cities.filters import (
    SubregionFilter,
    RegionFilter,
    CountryFilter,
    StateFilter,
    CityFilter,
)
from countries_states_cities.models import Region, Subregion, Country, State, City
from countries_states_cities.serializers import (
    RegionSerializer,
    SubregionSerializer,
    CountrySerializer,
    StateSerializer,
    CitySerializer,
)


# Variable Section
from countries_states_cities.utils import get_translated_fields


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
    qs = (
        queryset.filter(
            latitude__range=[
                Decimal(latitude - latitude_diff),
                Decimal(latitude + latitude_diff),
            ],
            longitude__range=[
                Decimal(longitude - longitude_diff),
                Decimal(longitude + longitude_diff),
            ],
        )
        .annotate(distance=distance_raw_sql)
        .order_by("distance")
    )

    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance)
    return qs


class DistanceOrdering(OrderingFilter):
    ordering_latitude_param = "latitude"
    ordering_latitude_description = "Latitude to sort."
    ordering_longitude_param = "longitude"
    ordering_longitude_description = "Longitude to sort."

    ordering_fields = ["location"]

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if not ordering:
            # implement a custom ordering here
            ordering = []

        if "location" in ordering:
            try:
                latitude = request.query_params.get(self.ordering_latitude_param)
                longitude = request.query_params.get(self.ordering_longitude_param)
                latitude = Decimal(latitude)
                longitude = Decimal(longitude)
                return sort_by_nearest(queryset, latitude, longitude)
            except Exception as e:
                print(e)
                ordering.remove("location")

        if ordering:
            return queryset.order_by(*ordering)

        return queryset

    def get_schema_fields(self, view):
        assert (
            coreapi is not None
        ), "coreapi must be installed to use `get_schema_fields()`"
        assert (
            coreschema is not None
        ), "coreschema must be installed to use `get_schema_fields()`"
        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location="query",
                schema=coreschema.String(
                    title=force_str(self.ordering_title),
                    description=force_str(self.ordering_description),
                ),
            ),
            coreapi.Field(
                name=self.ordering_latitude_param,
                required=False,
                location="query",
                schema=coreschema.String(
                    title=force_str(self.ordering_latitude_param),
                    description=force_str(self.ordering_latitude_description),
                ),
            ),
            coreapi.Field(
                name=self.ordering_longitude_param,
                required=False,
                location="query",
                schema=coreschema.String(
                    title=force_str(self.ordering_longitude_param),
                    description=force_str(self.ordering_longitude_description),
                ),
            ),
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": self.ordering_param,
                "required": False,
                "in": "query",
                "description": force_str(self.ordering_description),
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": self.ordering_latitude_param,
                "required": False,
                "in": "query",
                "description": force_str(self.ordering_latitude_description),
                "schema": {
                    "type": "string",
                },
            },
            {
                "name": self.ordering_longitude_param,
                "required": False,
                "in": "query",
                "description": force_str(self.ordering_longitude_description),
                "schema": {
                    "type": "string",
                },
            },
        ]


class ViewSetMixin(mixins.ListModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    filter_backends = [DistanceOrdering, filters.SearchFilter, DjangoFilterBackend]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_fields = self.get_search_fields()

    def get_search_fields(self):
        # get_translated_fields 함수를 사용하여 번역된 필드를 검색 필드에 포함시킵니다.
        translated_fields = get_translated_fields(self.model, "name")

        # 모델 별로 특정 검색 필드를 추가합니다.
        if self.model == Country:
            # 'Country' 모델에 대해 'phone_code' 필드를 추가합니다.
            return ("phone_code",) + translated_fields

        # 다른 모델에 대해서는 기본 번역 필드만 사용합니다.
        return translated_fields


class RegionViewSet(ViewSetMixin):
    model = Region
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = ViewSetMixin.filter_backends
    filterset_class = RegionFilter


class SubregionViewSet(ViewSetMixin):
    model = Subregion
    queryset = Subregion.objects.all()
    serializer_class = SubregionSerializer
    filterset_class = SubregionFilter


class CountryViewSet(ViewSetMixin):
    model = Country
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filterset_class = CountryFilter

    def get_default_ordering_field(self):
        """
        현재 언어에 맞는 정렬 필드를 반환하는 메서드
        ordering 파라미터 값이 없을 경우 반환되는 필드로 오더링 됩니다.
        """
        current_language = get_language()
        ordering_field = f"name_{current_language}"

        # 한국어 일 경우 collate 지정.
        try:
            if ordering_field == "name_ko":
                ordering_field = Func(
                    "name_ko",
                    function="ko_KR.utf8",
                    template='(%(expressions)s) COLLATE "%(function)s"',
                )
            # 일본어 일 경우 collate 지정
            elif ordering_field == "name_ja":
                ordering_field = Func(
                    "name_ja",
                    function="ja_JP.utf8",
                    template='(%(expressions)s) COLLATE "%(function)s"',
                )
            # 아랍어 일 경우 collate 지정
            elif ordering_field == "name_ar":
                ordering_field = Func(
                    "name_ar",
                    function="ar_SA.utf8",
                    template='(%(expressions)s) COLLATE "%(function)s"',
                )
        except Exception as e:
            print(f"{current_language} collate를 지원하지 않습니다.")
            print(e)
            return f"name_{current_language}"

        return ordering_field

    def get_queryset(self):
        ordering_field = self.get_default_ordering_field()
        self.queryset = self.model.objects.all().order_by(ordering_field)
        return super().get_queryset()


class StateViewSet(ViewSetMixin):
    model = State
    queryset = State.objects.all().order_by("-id")
    serializer_class = StateSerializer
    filterset_class = StateFilter


class CityViewSet(ViewSetMixin):
    model = City
    queryset = City.objects.all().order_by("-id")
    serializer_class = CitySerializer
    filterset_class = CityFilter
