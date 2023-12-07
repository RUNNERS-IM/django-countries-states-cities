from rest_framework import serializers
from countries_states_cities.models import Region, Subregion, Country, State, City


default_fields = ['id', 'name', 'name_en', 'name_ja', 'name_ko', 'wikiDataId']


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = default_fields


class SubregionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subregion
        fields = default_fields + ['region']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = default_fields + ['region', 'subregion', 'iso2', 'currency', 'currency_symbol', 'native', 'emoji']


class StateSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = State
        fields = default_fields + ['country', 'iso2']


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = City
        fields = default_fields + ['country', 'state']
