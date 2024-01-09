# Django
from django.conf import settings


def get_translated_fields(model, field_name):
    """ 모델의 특정 필드에 대한 번역 필드 이름을 튜플로 반환합니다. """
    translated_fields = [field_name]  # 기본 필드 추가

    for lang_code, lang_name in settings.LANGUAGES:
        translated_field = f"{field_name}_{lang_code}"

        if hasattr(model, translated_field):
            translated_fields.append(translated_field)

    return tuple(translated_fields)  # 튜플로 변환하여 반환
