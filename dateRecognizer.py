import re
from collections import defaultdict

months = [
    'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
    'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень',
    'Січ', 'Лют', 'Бер', 'Кві', 'Тра', 'Чер', 'Лип', 'Сер', 'Вер', 'Жов', 'Лис', 'Гру',
    'Січня', 'Лютого', 'Березня', 'Квітня', 'Травня', 'Червня', 'Липня', 'Серпня', 'Вересня', 'Жовтня', 'Листопада', 'Грудня'
]

ordinal_numbers = [
    'Перше', 'Друге', 'Третє', 'Четверте', 'П’яте', 'Шосте', 'Сьоме', 'Восьме', 'Дев’яте', 'Десяте',
    'Одинадцяте', 'Дванадцяте', 'Тринадцяте', 'Чотирнадцяте', 'П’ятнадцяте', 'Шістнадцяте', 'Сімнадцяте',
    'Вісімнадцяте', 'Дев’ятнадцяте', 'Двадцяте', 'Двадцять перше', 'Двадцять друге', 'Двадцять третє',
    'Двадцять четверте', 'Двадцять п’яте', 'Двадцять шосте', 'Двадцять сьоме', 'Двадцять восьме',
    'Двадцять дев’яте', 'Тридцяте', 'Тридцять перше',
    'Першого', 'Другого', 'Третього', 'Четвертого', 'П’ятого', 'Шостого', 'Сьомого', 'Восьмого', 'Дев’ятого', 'Десятого',
    'Одинадцятого', 'Дванадцятого', 'Тринадцятого', 'Чотирнадцятого', 'П’ятнадцятого', 'Шістнадцятого', 'Сімнадцятого',
    'Вісімнадцятого', 'Дев’ятнадцятого', 'Двадцятого', 'Двадцять першого', 'Двадцять другого', 'Двадцять третього',
    'Двадцять четвертого', 'Двадцять п’ятого', 'Двадцять шостого', 'Двадцять сьомого', 'Двадцять восьмого',
    'Двадцять дев’ятого', 'Тридцятого', 'Тридцять першого'
]
months += [month.lower() for month in months]
ordinal_numbers += [num.lower() for num in ordinal_numbers]

def escape_words(words):
    return [re.escape(word) for word in words]


month_pattern = r'\b(?:' + '|'.join(escape_words(months)) + r')\b'

ordinal_day_pattern = r'\b(?:' + '|'.join(escape_words(ordinal_numbers)) + r')\b'

numeric_day_pattern = r'\b(?:0?[1-9]|[12][0-9]|3[01])(?:st|nd|rd|th)?\b'

numeric_month_pattern = r'\b(?:0?[1-9]|1[012])\b'

year_pattern = r"\b\d{1,4}\b"

date_separators = r'[/\.-]'

# Компіляція regex

numeric_date_pattern = re.compile(
    r'\b(' + numeric_day_pattern + r')' + date_separators +
    r'(' + numeric_month_pattern + r')' + date_separators +
    r'(' + year_pattern + r')\b'
)

iso_date_pattern = re.compile(
    r'\b(' + year_pattern + r')' + date_separators +
    r'(' + numeric_month_pattern + r')' + date_separators +
    r'(' + numeric_day_pattern + r')\b'
)

us_date_pattern = re.compile(
    r'\b(' + numeric_month_pattern + r')' + date_separators +
    r'(' + numeric_day_pattern + r')' + date_separators +
    r'(' + year_pattern + r')\b'
)

ordinal_textual_date_pattern = re.compile(
    r'\b(' + ordinal_day_pattern + r')\s+of\s+(' + month_pattern + r')(?:,\s*(' + year_pattern + r'))?\b'
)


def read_text_from_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Файл {filepath} не знайдено.")
        return None


filepath = 'input_dates.txt'
text = read_text_from_file(filepath)

def first_pass(text):
    patterns = [
        ('NUMERIC_DATE', numeric_date_pattern),
        ('ISO_DATE', iso_date_pattern),
        ('US_DATE', us_date_pattern),
        ('ORDINAL_TEXTUAL_DATE', ordinal_textual_date_pattern),
        ('MONTH', re.compile(month_pattern)),
        ('ORDINAL_DAY', re.compile(ordinal_day_pattern)),
        ('NUMERIC_DAY', re.compile(numeric_day_pattern)),
        ('NUMERIC_MONTH', re.compile(numeric_month_pattern)),
        ('YEAR', re.compile(year_pattern)),
    ]

    matches = []
    for tag, regex in patterns:
        for match in regex.finditer(text):
            matches.append({
                'text': match.group(),
                'start': match.start(),
                'end': match.end(),
                'tag': tag
            })

    matches.sort(key=lambda x: (x['start'], -x['end']))
    non_overlapping = []
    occupied = [False] * len(text)
    for match in matches:
        if not any(occupied[match['start']:match['end']]):
            non_overlapping.append(match)
            for i in range(match['start'], match['end']):
                occupied[i] = True

    return non_overlapping

def second_pass(matches, text):
    date_tags = ['NUMERIC_DATE', 'ISO_DATE', 'US_DATE', 'TEXTUAL_DATE', 'ORDINAL_TEXTUAL_DATE']

    combined_matches = []
    i = 0
    while i < len(matches):
        match = matches[i]
        if match['tag'] in date_tags:
            combined_matches.append(match)
            i += 1
        else:
            # Намагаємося об'єднати день, місяць і рік у дату
            date_components = [match]
            i += 1
            while i < len(matches):
                next_match = matches[i]
                gap_text = text[date_components[-1]['end']:next_match['start']]
                if next_match['tag'] in ['NUMERIC_DAY', 'ORDINAL_DAY', 'NUMERIC_MONTH', 'MONTH', 'YEAR'] and \
                   re.match(r'^\s*(of\s+|,\s*|\s+)\s*$', gap_text):
                    date_components.append(next_match)
                    i += 1
                else:
                    break
            if len(date_components) > 1:
                start = date_components[0]['start']
                end = date_components[-1]['end']
                combined_text = text[start:end]
                combined_matches.append({
                    'text': combined_text,
                    'start': start,
                    'end': end,
                    'tag': 'DATE',
                    'components': date_components
                })
            else:
                combined_matches.append(match)
    return combined_matches


def third_pass(matches):
    date_entities = []
    for match in matches:
        if match['tag'] in ['NUMERIC_DATE', 'ISO_DATE', 'US_DATE', 'TEXTUAL_DATE', 'ORDINAL_TEXTUAL_DATE', 'DATE']:
            normalized_date = normalize_date(match)
            if normalized_date:
                date_entities.append(normalized_date)
    return date_entities


def normalize_date(match):
    text = match['text']
    tag = match['tag']

    try:
        day = month = year = None

        if tag == 'NUMERIC_DATE':
            result = numeric_date_pattern.match(text)
            if result:
                day, month, year = result.group(1), result.group(2), result.group(3)

        elif tag == 'ISO_DATE':
            result = iso_date_pattern.match(text)
            if result:
                year, month, day = result.group(1), result.group(2), result.group(3)

        elif tag == 'US_DATE':
            result = us_date_pattern.match(text)
            if result:
                month, day, year = result.group(1), result.group(2), result.group(3)
        elif tag == 'ORDINAL_TEXTUAL_DATE':
            result = ordinal_textual_date_pattern.match(text)
            if result:
                day_text, month_text, year = result.group(1), result.group(2), result.group(3)
                day = ordinal_to_number(day_text)
                month = month_to_number(month_text)
                year = year if year else '0000'

        elif tag == 'DATE':
            components = match['components']
            for comp in components:
                if comp['tag'] in ['NUMERIC_DAY', 'ORDINAL_DAY']:
                    day = ordinal_to_number(comp['text'])
                elif comp['tag'] in ['NUMERIC_MONTH', 'MONTH']:
                    month = month_to_number(comp['text'])
                elif comp['tag'] == 'YEAR':
                    year = comp['text']

        if not day:
            day = '00'
        if not month:
            month = '0'
        if not year:
            year = '0000'

        # Видаляємо суфікси з дня, прибираємо зайві нулі з місяця та року
        day = day.rstrip('stndrdth')
        month = month.lstrip('0')

        # Виправляємо нормалізацію для двозначних років
        if len(year) == 2:
            year = '00' + year

        normalized = f"{int(year):04d}-{int(month):02d}-{int(day):02d}"
        return {'original': text, 'normalized': normalized}
    except Exception as e:
        print(f"Помилка при нормалізації дати '{text}': {e}")
        return None


def month_to_number(month_name):
    month_name = month_name.lower()
    month_map = {
        'січень': '1', 'січ': '1', 'січня': '1',
        'лютий': '2', 'лют': '2', 'лютого': '2',
        'березень': '3', 'бер': '3', 'березня': '3',
        'квітень': '4', 'кві': '4', 'квітня': '4',
        'травень': '5', 'тра': '5', 'травня': '5',
        'червень': '6', 'чер': '6', 'червня': '6',
        'липень': '7', 'лип': '7', 'липня': '7',
        'серпень': '8', 'сер': '8', 'серпня': '8',
        'вересень': '9', 'вер': '9', 'вересня': '9',
        'жовтень': '10', 'жов': '10', 'жовтня': '10',
        'листопад': '11', 'лис': '11', 'листопада': '11',
        'грудень': '12', 'гру': '12', 'грудня': '12',
    }
    return month_map.get(month_name.lower(), '1')


def ordinal_to_number(ordinal):
    ordinal = ordinal.lower().replace('-', ' ')
    ordinal_map = {
        'перше': '1', 'друге': '2', 'третє': '3', 'четверте': '4', 'п’яте': '5',
        'шосте': '6', 'сьоме': '7', 'восьме': '8', 'дев’яте': '9', 'десяте': '10',
        'одинадцяте': '11', 'дванадцяте': '12', 'тринадцяте': '13', 'чотирнадцяте': '14',
        'п’ятнадцяте': '15', 'шістнадцяте': '16', 'сімнадцяте': '17', 'вісімнадцяте': '18',
        'дев’ятнадцяте': '19', 'двадцяте': '20', 'двадцять перше': '21',
        'двадцять друге': '22', 'двадцять третє': '23',
        'двадцять четверте': '24', 'двадцять п’яте': '25',
        'двадцять шосте': '26', 'двадцять сьоме': '27',
        'двадцять восьме': '28', 'двадцять дев’яте': '29',
        'тридцяте': '30', 'тридцять перше': '31',
        'першого': '1', 'другого': '2', 'третього': '3', 'четвертого': '4', 'п’ятого': '5',
        'шостого': '6', 'сьомого': '7', 'восьмого': '8', 'дев’ятого': '9', 'десятого': '10',
        'одинадцятого': '11', 'дванадцятого': '12', 'тринадцятого': '13', 'чотирнадцятого': '14',
        'п’ятнадцятого': '15', 'шістнадцятого': '16', 'сімнадцятого': '17', 'вісімнадцятого': '18',
        'дев’ятнадцятого': '19', 'двадцятого': '20', 'двадцять першого': '21',
        'двадцять другого': '22', 'двадцять третього': '23',
        'двадцять четвертого': '24', 'двадцять п’ятого': '25',
        'двадцять шостого': '26', 'двадцять сьомого': '27',
        'двадцять восьмого': '28', 'двадцять дев’ятого': '29',
        'тридцятого': '30', 'тридцять першого': '31'
    }
    return ordinal_map.get(ordinal.lower(), ordinal.rstrip('stndrdth'))


first_pass_matches = first_pass(text)
print("ПЕРШИЙ ПРОХІД: Знайдені сутності")
for match in first_pass_matches:
    print(f"[{match['tag']}] '{match['text']}' (позиції {match['start']}-{match['end']})")

combined_matches = second_pass(first_pass_matches, text)
print("\nДРУГИЙ ПРОХІД: Об'єднані дати")
for match in combined_matches:
    if 'components' in match:
        components = ', '.join([comp['text'] for comp in match['components']])
        print(f"[{match['tag']}] '{match['text']}' з компонентів [{components}]")
    else:
        print(f"[{match['tag']}] '{match['text']}'")

final_entities = third_pass(combined_matches)
print("\nТРЕТІЙ ПРОХІД: Нормалізовані дати")
for entity in final_entities:
    print(f"Оригінал: '{entity['original']}', Нормалізовано: '{entity['normalized']}'")


def group_dates(entities):
    grouped = defaultdict(list)
    for entity in entities:
        key = entity['normalized']
        grouped[key].append(entity['original'])
    return grouped


grouped_dates = group_dates(final_entities)
print("\nЗГРУПОВАНІ ДАТИ:")
for key, dates in grouped_dates.items():
    print(f"\nДата: {key}")
    for date in dates:
        print(f" - {date}")
