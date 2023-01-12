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
        get_translation(translation_card_json)
    )


UNIVERSAL_DICTIONARY_KEY = 'LingvoUniversal (En-Ru)'
BODY_KEY = "Body"
ITEMS_KEY = "Items"
MARKUP_KEY = "Markup"
TEXT_KEY = "Text"
NODE_KEY = "Node"
SPECIAL_CHARS = {'/', '\\', '-', ',', '.', ';', '\'', '-', '—', '(', ')', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
FATAL_CHARS = {'↑'}


def get_translation(translation_card_json):
    result = list()

    process_stack = list()
    for card in translation_card_json[::-1]:
        process_stack.append(card)

    element = process_stack.pop()
    while element is not None:
        if NODE_KEY in element and element[NODE_KEY] == "Text":
            result.append(element)

        append_children(BODY_KEY, element, process_stack)
        append_children(MARKUP_KEY, element, process_stack)
        append_children(ITEMS_KEY, element, process_stack)
        element = process_stack.pop() if len(process_stack) > 0 else None

    translations = filter_out(result)

    return translations


def filter_out(result):
    translations = list()
    for r in result:
        stripped = r[TEXT_KEY].strip()

        filtered = remove_start_special(stripped)
        while filtered != stripped:
            stripped = filtered
            filtered = remove_start_special(stripped)

        filtered = remove_end_special(stripped)
        while filtered != stripped:
            stripped = filtered
            filtered = remove_end_special(stripped)

        for fatal_char in FATAL_CHARS:
            filtered = filtered.replace(fatal_char, '')

        if len(filtered) > 0:
            translations.append(filtered)
    return translations


def remove_start_special(string):
    if len(string) > 0 and string[0] in SPECIAL_CHARS:
        string = string[1:len(string)].strip() if len(string) > 1 else ""
    return string


def remove_end_special(string):
    if len(string) > 0 and string[-1] in SPECIAL_CHARS:
        string = string[0:len(string) - 1].strip() if len(string) > 1 else ""
    return string


def append_children(key, element, process_stack):
    if key in element:
        children = element[key]
        for child in children[::-1]:
            process_stack.append(child)


# def find_element(elements, json_field_key, json_filed_value):
#     children = [x for x in elements if (json_field_key in x and x[json_field_key] == json_filed_value)]
#     if len(children) > 1:
#         print(f'There is find more than one child of {json_field_key}={json_filed_value}')
#     return children[0] if len(children) > 0 else None
#
#
# def extract_translation(translation_variant_json):
#     translation = ""
#     try:
#         markup = translation_variant_json[MARKUP_KEY]
#         print(f'markup = {markup}')
#         type_3_obj = find_element(markup, "Type", 3)
#         if type_3_obj is None:
#             """This is short translation card variant"""
#             last = markup[-1]
#             mr = last[MARKUP_KEY]
#             text_node = find_element(mr, "Node", "Text")
#             node = text_node
#             text = node[TEXT_KEY]
#         else:
#             items = type_3_obj[ITEMS_KEY]
#             for item in items:
#                 mr = item[MARKUP_KEY]
#                 paragraph = find_element(mr, "Node", "Paragraph")
#                 paragraph_markup = paragraph[MARKUP_KEY]
#                 text_node = find_element(paragraph_markup, "Node", "Text")
#                 text = text_node[TEXT_KEY]
#                 translation += f'{text}; '
#     except:
#         pass
#
#     return translation


def authorize():
    response = requests.post(LINGVO_AUTH, headers={"Authorization": f'Basic {API_KEY}'})
    bearer = response.text
    print(f'Bearer token: {bearer}')
    return bearer
