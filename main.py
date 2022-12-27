from dictionary import save_dictionary, load_dictionary, backup
from subtitles import load_uniq_words_from_subtitles_srt

add_sign = '+'


def build_new_words_dict(learned_dictionary_fn, subtitle_fn):
    learned_dictionary = load_dictionary(learned_dictionary_fn)
    print(f'Dictionary size is {len(learned_dictionary)}')
    # print("Dictionary's elements: {}".format(learned_dictionary))

    loaded_uniq_words = load_uniq_words_from_subtitles_srt(subtitle_fn)
    return loaded_uniq_words.difference(learned_dictionary)


def update_learned_dictionary(learned_dictionary_fn, learning_words_fn):
    backup(learned_dictionary_fn)

    learned_dictionary = load_dictionary(learned_dictionary_fn)
    print(f'Dictionary size is {len(learned_dictionary)}')
    # print("Dictionary's elements: {}".format(learned_dictionary))

    learning_words = load_dictionary(learning_words_fn)
    new_words = extract_new_words(learning_words)
    return learned_dictionary.union(new_words)


def extract_new_words(learning_words):
    new_words = set()
    for word in learning_words:
        if word.strip().startswith(add_sign):
            new_words.add(word.removeprefix(add_sign))
    return new_words


if __name__ == '__main__':
    # todo introduce commands
    cmd = "new_words"
    # cmd = "update_dict"

    dictionary_fn = "dictionary\\dictionary.txt"
    source_fn = "sources\\Rio.DVDRip.XviD-ZMG.srt"

    new_words_fn = "dictionary\\new_words_from_{}.txt".format(source_fn.split(sep="\\")[-1])

    if cmd == "new_words":
        uniq_words_to_learn = build_new_words_dict(dictionary_fn, source_fn)
        save_dictionary(uniq_words_to_learn, new_words_fn)
    else:
        updated_dictionary = update_learned_dictionary(dictionary_fn, new_words_fn)
        save_dictionary(updated_dictionary, dictionary_fn)
