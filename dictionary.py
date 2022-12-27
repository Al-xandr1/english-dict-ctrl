from shutil import copyfile

from sortedcontainers import SortedDict


def save_dictionary(dictionary, dictionary_fn):
    sorted_dictionary = SortedDict()
    for word in dictionary:
        sorted_dictionary[word] = word

    f = open(dictionary_fn, 'w')
    for word in sorted_dictionary:
        striped = word.strip()
        if not striped:
            continue
        f.write("{}\n".format(striped))
    f.close()


def load_dictionary(learned_dictionary_fn):
    dictionary_file = open(learned_dictionary_fn, 'r')
    dictionary = set()
    while True:
        word = dictionary_file.readline()
        if not word:
            break
        stripped = word.strip()
        if stripped:
            dictionary.add(stripped)
    dictionary_file.close()
    return dictionary


def backup(learned_dictionary):
    copyfile(learned_dictionary, "{}_backup".format(learned_dictionary))
