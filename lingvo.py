import requests

from dictionary import DICT_FORMAT, load_dictionary

LINGVO_SITE_URL = "https://www.lingvolive.com/en-us/translate/en-ru/{}"
TRANSLATION_CARD_PATTER = "<a href=\"{}\">{}</a><br>"

LINGVO_BASE_URL = "https://developers.lingvolive.com"
API_KEY = "MmY3Mzg5ODYtNWI1ZC00YmM4LWFjNDMtNTNhOGRhMmE5YzcwOjRiOTUyMzgxYTJiNDRlNmZhMGQyMTA0NTcwOWM1Y2Ez"

LINGVO_AUTH = LINGVO_BASE_URL + "/api/v1.1/authenticate"
LINGVO_TRANSLATION = LINGVO_BASE_URL + "/api/v1/Translation?text={}&srcLang=1033&dstLang=1049"


def translate_words(words_set):
    """:returns build dict container of translated words"""

    token = authorize()
    translated_words = dict()
    for word in words_set:
        translation_card = build_translation_card(word, token)
        print(DICT_FORMAT.format(word, translation_card))
        translated_words[word] = translation_card
    return translated_words


def translate_dict(dictionary_fn):
    dictionary = load_dictionary(dictionary_fn)
    token = authorize()
    for word, old_translation_card in dictionary.items():
        translation_card = build_translation_card(word, token)
        print(DICT_FORMAT.format(word, translation_card))
        dictionary[word] = translation_card
    return dictionary


def build_translation_card(english_word, token):
    # response = requests.get(LINGVO_TRANSLATION.format(english_word), headers={"Authorization": f'Bearer {token}'})
    # todo make json parsing
    # translation_card = response.json()
    # print(f'Received json: {translation_card}')

    return TRANSLATION_CARD_PATTER.format(
        LINGVO_SITE_URL.format(english_word),
        english_word
    )


def authorize():
    response = requests.post(LINGVO_AUTH, headers={"Authorization": f'Basic {API_KEY}'})
    bearer = response.text
    print(f'Bearer token: {bearer}')
    return bearer
