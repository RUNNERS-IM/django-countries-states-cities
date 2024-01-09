from django.db import models


# Class Section
class BaseArea(models.Model):

    # Basic
    name = models.CharField(max_length=255)

    # Numbers
    flag = models.IntegerField(null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)

    # Data
    wikiDataId = models.CharField(max_length=255, blank=True, null=True)
    translations = models.TextField(blank=True, null=True)

    # Dates
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)


class Region(BaseArea):

    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regions'
        ordering = ['-created_at']


class Subregion(BaseArea):
    # FK
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL, )

    class Meta:
        verbose_name = 'subregion'
        verbose_name_plural = 'subregions'
        ordering = ['-created_at']


class Country(BaseArea):
    # FK
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL, )
    subregion = models.ForeignKey(Subregion, null=True, on_delete=models.SET_NULL, )

    # Basic
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    numeric_code = models.CharField(max_length=3, blank=True, null=True)
    iso2 = models.CharField(max_length=2, blank=True, null=True)
    phone_code = models.CharField(max_length=255, blank=True, null=True)
    capital = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=255, blank=True, null=True)
    currency_name = models.CharField(max_length=255, blank=True, null=True)
    currency_symbol = models.CharField(max_length=255, blank=True, null=True)
    tld = models.CharField(max_length=255, blank=True, null=True)
    native = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    timezones = models.TextField(blank=True, null=True)
    emoji = models.CharField(max_length=255, blank=True, null=True)
    emojiU = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'
        ordering = ['-created_at']


class State(BaseArea):
    # FK
    country = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL, )
    country_code = models.CharField(max_length=2, blank=True, null=True)
    country_name = models.CharField(max_length=255, blank=True, null=True)

    # Basic
    state_code = models.CharField(max_length=255, blank=True, null=True)

    fips_code = models.CharField(max_length=255, blank=True, null=True)
    iso2 = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        verbose_name = 'state'
        verbose_name_plural = 'states'
        ordering = ['-created_at']


class City(BaseArea):
    # FK
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, )
    country_code = models.CharField(max_length=2, blank=True, null=True)
    country_name = models.CharField(max_length=255, blank=True, null=True)

    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, )
    state_code = models.CharField(max_length=255, blank=True, null=True)
    state_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'
        ordering = ['-created_at']