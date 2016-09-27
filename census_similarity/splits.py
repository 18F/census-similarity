import re


non_letter_digit = re.compile('[^A-Z0-9]')


def character(text):
    return non_letter_digit.sub('', text.upper())


def bigram(text):
    text = character(text)
    return tuple(text[2*i:2*i+2] for i in range(0, len(text), 2))


def trigram(text):
    text = character(text)
    return tuple(text[3*i:3*i+3] for i in range(0, len(text), 3))


def comma(text):
    components = (el.strip() for el in text.split(','))
    return tuple(filter(bool, components))
