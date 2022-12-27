from lexem import clean_up


def load_uniq_words_from_subtitles_srt(subtitle_fn):
    f = open("%s" % subtitle_fn, 'r')
    uniq_words = set()
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
                uniq_words.add(word.lower())
    f.close()

    print("Total number of replicas in the subtitle file is {}".format(replica_numbers))
    print(f'Subtitles\' uniq words count is {len(uniq_words)}')
    # print("Subtitles\' elements: {}".format(uniq_words))

    return uniq_words
