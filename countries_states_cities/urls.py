from django.urls import path
from rest_framework.routers import DefaultRouter

from countries_states_cities import views
from countries_states_cities.views import RegionViewSet, SubregionViewSet, CountryViewSet, StateViewSet, CityViewSet

router = DefaultRouter()
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'subregions', SubregionViewSet, basename='subregion')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'states', StateViewSet, basename='state')
router.register(r'cities', CityViewSet, basename='city')
urlpatterns = router.urls


urlpatterns += [
    # path('search', views.SearchView, name='regions'),
]