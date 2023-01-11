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
    response = requests.get(LINGVO_TRANSLATION.format(english_word), headers={"Authorization": f'Bearer {token}'})
    translation_card_json = response.json()
    # print(f'Received json: {translation_card_json}')

    return TRANSLATION_CARD_PATTER.format(
        LINGVO_SITE_URL.format(english_word),
        english_word  # todo get_translation(translation_card_json)
    )


UNIVERSAL_DICTIONARY = 'LingvoUniversal (En-Ru)'
BODY = "Body"
ITEMS = "Items"
MARKUP = "Markup"
TEXT = "Text"


def get_translation(translation_card_json):
    """TODO make recursive traversing of JSON with capture all TEXT nodes """

    universal_card = find_element(translation_card_json, "Dictionary", UNIVERSAL_DICTIONARY)
    top_level_body = universal_card[BODY]
    type_2_obj = find_element(top_level_body, "Type", 2)

    # list of translations
    translations_list_json = type_2_obj[ITEMS]
    translations = list()
    for translation_variant in translations_list_json:
        translations.append(extract_translation(translation_variant))

    return translations


def find_element(elements, json_field_key, json_filed_value):
    children = [x for x in elements if (json_field_key in x and x[json_field_key] == json_filed_value)]
    if len(children) > 1:
        print(f'There is find more than one child of {json_field_key}={json_filed_value}')
    return children[0] if len(children) > 0 else None


def extract_translation(translation_variant_json):
    translation = ""
    try:
        markup = translation_variant_json[MARKUP]
        print(f'markup = {markup}')
        type_3_obj = find_element(markup, "Type", 3)
        if type_3_obj is None:
            """This is short translation card variant"""
            last = markup[-1]
            mr = last[MARKUP]
            text_node = find_element(mr, "Node", "Text")
            node = text_node
            text = node[TEXT]
        else:
            items = type_3_obj[ITEMS]
            for item in items:
                mr = item[MARKUP]
                paragraph = find_element(mr, "Node", "Paragraph")
                paragraph_markup = paragraph[MARKUP]
                text_node = find_element(paragraph_markup, "Node", "Text")
                text = text_node[TEXT]  # TODO it may be wrong word. It should process all elements in the current item
                translation += f'{text}; '
    except:
        pass

    return translation


def authorize():
    response = requests.post(LINGVO_AUTH, headers={"Authorization": f'Basic {API_KEY}'})
    bearer = response.text
    print(f'Bearer token: {bearer}')
    return bearer
