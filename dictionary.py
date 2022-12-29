from shutil import copyfile

from sortedcontainers import SortedDict

add_sign = '+'
dict_separator = "->"
dict_format = "{}\t\t" + dict_separator + "\t{}\n"


def save_dictionary(dictionary, dictionary_fn):
    sorted_dictionary = SortedDict()
    for word, translate_card in dictionary.items():
        sorted_dictionary[word] = translate_card

    with open(dictionary_fn, 'w') as f:
        for word, translate_card in sorted_dictionary.items():
            striped = word.strip()
            if not striped:
                continue
            f.write(dict_format.format(striped, translate_card))


def load_dictionary(learned_dictionary_fn):
    dictionary = dict()
    with open(learned_dictionary_fn, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            dict_entry = line.split(sep=dict_separator)
            word = dict_entry[0].strip()
            translation_card = dict_entry[1] if len(dict_entry) > 1 else ""
            if word:
                dictionary[word] = translation_card.strip()
    return dictionary


def backup(learned_dictionary):
    copyfile(learned_dictionary, "{}_backup".format(learned_dictionary))


def extract_new_words_set(learning_words_set):
    new_words = set()
    for word in learning_words_set:
        if word.strip().startswith(add_sign):
            new_words.add(word.removeprefix(add_sign))
    return new_words
