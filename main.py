from sortedcontainers import SortedDict
from shutil import *
import string

add_sign = '+'
alphabetic = set(string.ascii_letters)


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_new_words(sbtl_name, learned_dictionary):
    learned_dictionary = load_dictionary(learned_dictionary)
    print(f'Dictionary size is {len(learned_dictionary)}')
    print("Dictionary's elements: {}".format(learned_dictionary))

    loaded_uniq_words = load_uniq_words_from_subtitles_srt(sbtl_name)
    uniq_words_to_learn = loaded_uniq_words.difference(learned_dictionary)
    save_dictionary(uniq_words_to_learn, "new_words_from_{}.txt".format(sbtl_name))


def update_learned_dictionary(learned_dictionary_filename, learning_words_filename):
    # todo test this method
    backup(learned_dictionary_filename)

    learned_dictionary = load_dictionary(learned_dictionary_filename)
    print(f'Dictionary size is {len(learned_dictionary)}')
    print("Dictionary's elements: {}".format(learned_dictionary))

    learning_words = load_dictionary(learning_words_filename)
    new_words = extract_new_words(learning_words)
    learned_dictionary.update(new_words)
    save_dictionary(learned_dictionary, learned_dictionary_filename)


def extract_new_words(learning_words):
    new_words = set()
    for word in learning_words:
        if word.strip().startswith(add_sign):
            new_words.add(word.removeprefix(add_sign))
    return new_words


def backup(learned_dictionary):
    copyfile(learned_dictionary, "{}_backup".format(learned_dictionary))


def load_uniq_words_from_subtitles_srt(subtitle_filename):
    f = open("%s" % subtitle_filename, 'r')
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


def save_dictionary(dictionary, dictionary_filename):
    sorted_dictionary = SortedDict()
    for word in dictionary:
        sorted_dictionary[word] = word

    f = open(dictionary_filename, 'w')
    for word in sorted_dictionary:
        striped = word.strip()
        if not striped:
            continue
        f.write("{}\n".format(striped))
    f.close()


def load_dictionary(learned_dictionary):
    dictionary_file = open(learned_dictionary, 'r')
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
    get_new_words("Rio.DVDRip.XviD-ZMG.srt", "dictionary.txt")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
