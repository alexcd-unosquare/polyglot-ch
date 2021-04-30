from typing import List

import requests
import random
from models import Word


def get_def(word: str, lang='en_US'):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/{lang}/{word}'
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as err:
        raise SystemError(err)
    if r.status_code != 200:
        return False, {}
    d = r.json()
    if not (meanings := d[0]['meanings']):
        return False, {}
    definitions = [elem['definition'] for elem in meanings[0]['definitions'] if 'definition' in elem]
    examples = [elem['example'] for elem in meanings[0]['definitions'] if 'example' in elem]
    return True, Word(name=d[0]['word'], definition=''.join(definitions), example=''.join(examples), learned=False, times_seen=0)


def get_words(num: int, file: bytes, lang='en_US'):
    words = []
    words_file = open(f'dictionaries/{lang}.txt', 'r')
    all_words = [word.strip() for word in words_file.readlines()]
    while num > 0:
        word = random.choice(all_words)
        valid, definition = get_def(word, lang)
        if not valid:
            continue
        words.append(definition)
        num -= 1
    words_file.close()
    return words


def get_words_from_file(lang='en_US'):
    words = []
    words_file = open(f'dictionaries/{lang}.txt', 'r')
    all_words = [word.strip() for word in words_file.readlines()]
    for word in all_words:
        valid, definition = get_def(word, lang)
        if not valid:
            continue
        words.append(definition)
    #words_file.close()
    return words
