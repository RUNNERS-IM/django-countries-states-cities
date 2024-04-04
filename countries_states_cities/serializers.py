# serializers.py

# Django
from django.utils.translation import get_language

# Django Rest Framework
from rest_framework import serializers

# Apps
from countries_states_cities.models import Region, Subregion, Country, State, City


default_fields = ['id', 'wikiDataId']


class AutoTranslateSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        current_language = get_language()
        name_field = f"name_{current_language}"

        if hasattr(instance, name_field):
            representation['name'] = getattr(instance, name_field)
        else:
            representation['name'] = instance.name

        return representation


class RegionSerializer(AutoTranslateSerializer):

    class Meta:
        model = Region
        fields = default_fields


class SubregionSerializer(AutoTranslateSerializer):
    class Meta:
        model = Subregion
        fields = default_fields + ['region']


class CountrySerializer(AutoTranslateSerializer):
    class Meta:
        model = Country
        fields = default_fields + ['region', 'subregion', 'iso2', 'phone_code']


class StateSerializer(AutoTranslateSerializer):
    country = CountrySerializer()

    class Meta:
        model = State
        fields = default_fields + ['country', 'iso2']


class CitySerializer(AutoTranslateSerializer):
    state = StateSerializer()

    class Meta:
        model = City
        fields = default_fields + ['country', 'state']
