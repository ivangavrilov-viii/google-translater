import asyncio


def translate_word(google_translator, name_string, new_language) -> str:
    to_translated_list, translated_list = list(), list()
    start_spec_word = False

    if not name_string or name_string is None:
        return None

    while "{" in name_string and '}' in name_string:
        start_index = 0
        for letter_index in range(len(name_string)):
            if not start_spec_word and name_string[letter_index] == '{':
                start_index = letter_index
                start_spec_word = True
            elif start_spec_word and name_string[letter_index] == '}':
                to_translated_list.append(name_string[:start_index])
                to_translated_list.append(name_string[start_index:letter_index + 1])
                name_string = name_string[letter_index + 1:]
                start_spec_word = False
                break
    else:
        to_translated_list.append(name_string)

    for word in to_translated_list:
        if "{" not in word and '}' not in word:
            loop = asyncio.get_event_loop()
            translated_text = loop.run_until_complete(google_translator.translate(word, dest=new_language))
            translated_list.append(translated_text.text)
        else:
            translated_list.append(word)

    return ' '.join(translated_list)
