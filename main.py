from sortedcontainers import SortedDict
from shutil import *
import string

add_sign = '+'
alphabetic = set(string.ascii_letters)


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def build_new_words_dict(learned_dictionary_fn, subtitle_fn):
    learned_dictionary_fn = load_dictionary(learned_dictionary_fn)
    print(f'Dictionary size is {len(learned_dictionary_fn)}')
    print("Dictionary's elements: {}".format(learned_dictionary_fn))

    loaded_uniq_words = load_uniq_words_from_subtitles_srt(subtitle_fn)
    return loaded_uniq_words.difference(learned_dictionary_fn)


def update_learned_dictionary(learned_dictionary_fn, learning_words_fn):
    backup(learned_dictionary_fn)

    learned_dictionary = load_dictionary(learned_dictionary_fn)
    print(f'Dictionary size is {len(learned_dictionary)}')
    print("Dictionary's elements: {}".format(learned_dictionary))

    learning_words = load_dictionary(learning_words_fn)
    new_words = extract_new_words(learning_words)
    return learned_dictionary.union(new_words)


def extract_new_words(learning_words):
    new_words = set()
    for word in learning_words:
        if word.strip().startswith(add_sign):
            new_words.add(word.removeprefix(add_sign))
    return new_words


def backup(learned_dictionary):
    copyfile(learned_dictionary, "{}_backup".format(learned_dictionary))


def load_uniq_words_from_subtitles_srt(subtitle_fn):
    f = open("%s" % subtitle_fn, 'r')
    sbtl_uniq_words = set()
    replica_numbers = 0
    while True:
        line = f.readline()
        if not line:
            break

        stripped = line.strip()
        if stripped.isdigit():
            replica_numbers = int(stripped)
            continue

        if "-->" in line:
            continue

        line_lexemes = stripped.split()
        for lexeme in line_lexemes:
            word = clean_up(lexeme)
            if word:
                sbtl_uniq_words.add(word)

    f.close()

    print("Total number of replicas in the subtitle file is {}".format(replica_numbers))
    print(f'Subtitles\' uniq words count is {len(sbtl_uniq_words)}')
    print("Subtitles\' elements: {}".format(sbtl_uniq_words))

    return sbtl_uniq_words


def clean_up(lexeme):
    first_index = find_first_alphabetic(lexeme)
    last_index = find_last_alphabetic(lexeme)
    return lexeme[first_index:last_index + 1]


def find_first_alphabetic(lexeme):
    first_index = 0
    for letter in lexeme:
        if letter not in alphabetic:
            first_index += 1
        else:
            break
    return first_index


def find_last_alphabetic(lexeme):
    first_index = find_first_alphabetic(reversed(lexeme))
    return len(lexeme) - first_index - 1


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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # todo introduce commands
    cmd = "new_words"
    # cmd = "update_dict"

    target_dictionary_fn = "dictionary.txt"
    new_words_source_fn = "Rio.DVDRip.XviD-ZMG.srt"
    new_words_fn = "new_words_from_{}.txt".format(new_words_source_fn)

    if cmd == "new_words":
        uniq_words_to_learn = build_new_words_dict(target_dictionary_fn, new_words_source_fn)
        save_dictionary(uniq_words_to_learn, new_words_fn)
    else:
        updated_dictionary = update_learned_dictionary(target_dictionary_fn, new_words_fn)
        save_dictionary(updated_dictionary, target_dictionary_fn)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
