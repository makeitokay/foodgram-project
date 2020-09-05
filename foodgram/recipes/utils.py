from django.utils.text import slugify

russian_alphabet = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ы": "y",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def russian_slugify(text):
    return slugify("".join(russian_alphabet.get(s, s) for s in text.lower()))


def filter_by_key(obj, query):
    """Return values from dict `obj` which keys start with `query`"""
    filtered_items = filter(lambda e: e[0].startswith(query), obj.items())
    return [v for k, v in filtered_items]
