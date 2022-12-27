import string


alphabetic = set(string.ascii_letters)


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


def clean_up(lexeme):
    first_index = find_first_alphabetic(lexeme)
    last_index = find_last_alphabetic(lexeme)
    return lexeme[first_index:last_index + 1]
