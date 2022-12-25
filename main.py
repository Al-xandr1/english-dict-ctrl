from sortedcontainers import SortedDict
from shutil import *
import string

alphabetic = set(string.ascii_letters)


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def backup(learned_dictionary):
    copyfile(learned_dictionary, "{}_backup".format(learned_dictionary))
    pass


def execute(sbtl_name, learned_dictionary):
    backup(learned_dictionary)

    dictionary = load_dictionary(learned_dictionary)
    print(f'Dictionary size is {len(dictionary)}')
    print("Dictionary's elements: {}".format(dictionary))

    uniq_words = load_uniq_words_from_subtitles_srt(sbtl_name)
    dictionary.update(uniq_words)
    save_dictionary(dictionary, learned_dictionary)


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

    f = open("{}_updated".format(dictionary_filename), 'w')
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
    execute("Rio.DVDRip.XviD-ZMG.srt", "dictionary.txt")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
