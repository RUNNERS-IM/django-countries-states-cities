# Django
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

# Utils
from countries_states_cities.utils import get_wikidata_translation, get_wikidata_id


# Class Section
class BaseAreaManager(models.Manager):
    def find_duplicates(self):
        # wikiDataId가 중복되는 객체들의 ID를 반환합니다.
        duplicates = self.values('wikiDataId') \
                         .annotate(wikiDataId_count=Count('id')) \
                         .filter(wikiDataId_count__gt=1) \
                         .values_list('wikiDataId', flat=True)
        return duplicates


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

    # Booleans
    is_duplicated = models.BooleanField(default=False)

    objects = BaseAreaManager()

    class Meta:
        abstract = True

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)

    def translate(self, is_save=True):
        if not self.wikiDataId:
            raise ValueError("No Wikidata ID provided")

        languages = [code for code, _ in settings.LANGUAGES]
        translations = get_wikidata_translation(self.wikiDataId, languages)
        translation_text_en = translations.get("en", "")

        # 중복된 객체인 경우
        if self.is_duplicated:
            name_old = self.name.lower()
            name_new = translation_text_en.lower()
            # 영문 이름이 현재 이름과 같으면 중복 해제
            if name_old == name_new or (name_old in name_new) or (name_new in name_old):
                self.is_duplicated = False
            else:
                return

        self.translations = translations

        # 언어별 필드에 번역 저장
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == 'en':
                continue

            translated_text = translations.get(lang_code, None)
            if not translated_text:
                translated_text = translation_text_en
            setattr(self, f'name_{lang_code}', translated_text)

        if is_save:
            self.save()

    def save(self, *args, **kwargs):
        # # wikiDataId 변경 여부 및 중복 상태 변경을 확인하기 위한 플래그
        # wikiDataId_changed = False
        # was_duplicated = self.is_duplicated
        #
        # # 기존 인스턴스가 있는 경우, 변경 여부를 체크합니다.
        # if self.pk:
        #     old_instance = type(self).objects.get(pk=self.pk)
        #     wikiDataId_changed = old_instance.wikiDataId != self.wikiDataId
        #     was_duplicated = old_instance.is_duplicated
        #
        # # 중복 여부를 업데이트합니다.
        # if wikiDataId_changed:
        #     self.update_duplicated_status(is_save=False)
        #
        # # 중복 상태가 변경되었거나 wikiDataId가 변경되었으면 번역을 수행합니다.
        # if wikiDataId_changed or was_duplicated != self.is_duplicated:
        #     self.translate(is_save=False)

        super().save(*args, **kwargs)

    def update_duplicated_status(self, is_save=True):
        # 다른 객체와 wikiDataId가 중복되는지 확인합니다.
        duplicate_exists = type(self).objects \
            .exclude(pk=self.pk) \
            .filter(wikiDataId=self.wikiDataId) \
            .exists()
        self.is_duplicated = duplicate_exists
        if is_save:
            self.save()

    def update_wikidata_id(self, is_save=True):
        if not self.is_duplicated:
            return

        new_wikidata_id = get_wikidata_id(self.name)
        if new_wikidata_id and new_wikidata_id != self.wikiDataId:
            self.wikiDataId = new_wikidata_id
            if is_save:
                self.save()


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
