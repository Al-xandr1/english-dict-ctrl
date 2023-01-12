from dictionary import save_dictionary, load_dictionary, backup, extract_new_words_set
from lingvo import translate_words, translate_dict, build_translation_card, authorize, get_translation
from subtitles import load_uniq_words_from_subtitles_srt


def build_new_words_set(learned_dictionary_fn, subtitle_fn):
    """:returns build set container of new words"""

    learned_dictionary = load_dictionary(learned_dictionary_fn)
    print(f'First loaded dictionary size is {len(learned_dictionary)}')

    loaded_uniq_words = load_uniq_words_from_subtitles_srt(subtitle_fn)
    return loaded_uniq_words.difference(learned_dictionary.keys())


def update_learned_dictionary(learned_dictionary_fn, learning_words_fn):
    backup(learned_dictionary_fn)

    learned_dictionary = load_dictionary(learned_dictionary_fn)
    print(f'Learned dictionary size is {len(learned_dictionary)}')

    learning_words = load_dictionary(learning_words_fn)
    print(f'Learning words size is {len(learning_words)}')

    new_words = extract_new_words_set(learning_words.keys())
    translated_words = translate_words(new_words)
    return learned_dictionary | translated_words


if __name__ == '__main__':
    # todo introduce commands
    # cmd = "new_words"
    # cmd = "update_dict"
    cmd = "translate_dict"

    dictionary_fn = "dictionary\\dictionary.html"
    source_fn = "sources\\Rio.DVDRip.XviD-ZMG.srt"

    new_words_fn = "dictionary\\new_words_from_{}.html".format(source_fn.split(sep="\\")[-1])

    if cmd == "new_words":
        new_words_to_learn = build_new_words_set(dictionary_fn, source_fn)
        translated_dictionary = translate_words(new_words_to_learn)
        save_dictionary(translated_dictionary, new_words_fn)

    elif cmd == "update_dict":
        updated_dictionary = update_learned_dictionary(dictionary_fn, new_words_fn)
        save_dictionary(updated_dictionary, dictionary_fn)

    elif cmd == "translate_dict":
        translated_dictionary = translate_dict(dictionary_fn)
        save_dictionary(translated_dictionary, dictionary_fn)

        # FOR TEST ONLY
        # token = authorize()
        # word = "murder"
        # translation_card = build_translation_card(word, token)
        # print(f'{word} -> {translation_card}')
        pass
