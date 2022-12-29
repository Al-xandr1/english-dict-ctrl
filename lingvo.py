import requests

from dictionary import dict_format, load_dictionary


def translate_words(words_set):
    """:returns build dict container of translated words"""
    translated_words = dict()
    for word in words_set:
        translation_card = translate(word)
        print(dict_format.format(word, translation_card))
        translated_words[word] = translation_card
    return translated_words


def translate_dict(dictionary_fn):
    dictionary = load_dictionary(dictionary_fn)
    for word, old_translation_card in dictionary.items():
        translation_card = translate(word)
        print(dict_format.format(word, translation_card))
        dictionary[word] = translation_card
    return dictionary


def translate(english_word):
    # api_url = "https://jsonplaceholder.typicode.com/todos/1"
    # response = requests.get(api_url)
    # json = response.json()
    # print(f'Received json: {json}')
    return english_word[::-1]
