# Python
import requests

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


def get_wikidata_translation(wikidata_id, languages):
    url = f"https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": wikidata_id,
        "format": "json",
        "props": "labels",
        "languages": "|".join(languages),
    }
    response = requests.get(url, params=params)
    data = response.json()

    translations = {}
    if 'entities' in data and wikidata_id in data['entities']:
        labels = data['entities'][wikidata_id].get('labels', {})
        for lang in languages:
            if lang in labels:
                translations[lang] = labels[lang]['value']

    print('[get_wikidata_translation] translations: ', translations)
    return translations


def get_wikidata_id(name):
    endpoint_url = "https://query.wikidata.org/sparql"
    query = f"""
    SELECT ?item WHERE {{
      ?item ?label "{name}"@en.
      ?item wdt:P31/wdt:P279* wd:Q618123.
      ?article schema:about ?item;
               schema:isPartOf <https://en.wikipedia.org/>.
    }} LIMIT 1
    """
    headers = {"Accept": "application/sparql-results+json"}
    response = requests.get(endpoint_url, params={"query": query}, headers=headers)

    # 조건이 충족되지 않으면 바로 None 반환
    if response.status_code != 200:
        return None

    data = response.json()
    results = data.get("results", {}).get("bindings", [])

    # 결과가 없으면 바로 None 반환
    if not results:
        return None

    wikidata_url = results[0].get("item", {}).get("value", None)
    # wikidata_url이 없으면 바로 None 반환
    if not wikidata_url:
        return None

    # URL에서 ID 부분만 추출
    wikidata_id = wikidata_url.split('/')[-1]
    print('[get_wikidata_id] wikidata_id: ', wikidata_id)
    return wikidata_id
