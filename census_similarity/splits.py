"""Methods to split a field into components"""
import re


non_letter_digit = re.compile('[^A-Z0-9]')


def character(text):
    """Sequence of characters"""
    return non_letter_digit.sub('', text.upper())


def bigram(text):
    """Sequence of bigrams, pairs of adjacent characters"""
    text = character(text) + " "
    return tuple(text[i:i+2] for i in range(len(text) - 2))


def trigram(text):
    """Sequence of trigrams, triplet of adjacent characters"""
    text = character(text) + "  "
    return tuple(text[i:i+3] for i in range(len(text) - 3))


def comma(text):
    """Split a string into components by exploding on a comma"""
    components = (el.strip() for el in text.split(','))
    return tuple(filter(bool, components))
