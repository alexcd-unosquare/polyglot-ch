import requests
from models import Word


# Gets definition and examples using the least problematic api I could find.
def get_def(word: str, lang='en_US'):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/{lang}/{word}'

    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as err:
        raise SystemError(err)
    if r.status_code != 200:
        return None

    d = r.json()
    if not (meanings := d[0]['meanings']):
        return None

    definitions = [elem['definition'] for elem in meanings[0]['definitions'] if 'definition' in elem]
    examples = [elem['example'] for elem in meanings[0]['definitions'] if 'example' in elem]

    if not definitions or not examples:
        return None
    return {'name': d[0]['word'], 'definition': ''.join(definitions), 'example': ''.join(examples), 'learned': False, 'times_seen': 0}
    #return Word(name=d[0]['word'], definition=''.join(definitions), example=''.join(examples), learned=False, times_seen=0)


def get_words_from_file(lang='en_US'):
    words = []
    words_file = open(f'dictionaries/{lang}.txt', 'r')
    all_words = list(set([word.strip() for word in words_file.readlines()]))[:150]

    for word in all_words:
        definition = get_def(word, lang)
        if definition is None:
            continue
        words.append(definition)
    return words
