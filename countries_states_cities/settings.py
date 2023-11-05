from django.conf import settings

LANGUAGES = getattr(settings, "LANGUAGES", None)
MODELTRANSLATION_DEFAULT_LANGUAGE = getattr(settings, "MODELTRANSLATION_DEFAULT_LANGUAGE", None)
