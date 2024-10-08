import re

def load_unique_cities(filepath):
    cities = set()
    with open(filepath, 'r') as file:
        for line in file:
            columns = line.strip().split('|')
            if columns:
                city = columns[0]
                cities.add(city)
    return list(cities)


def load_unique_counties(filepath):
    counties = set()
    with open(filepath, 'r') as file:
        for line in file:
            columns = line.strip().split('|')
            if columns:
                county = columns[0]
                counties.add(county)
    return list(counties)


class TextProcessor:
    def __init__(self):
        self.patterns = []

        # Loading cities
        filepath = 'cities.csv'
        cities = load_unique_cities(filepath)
        for city in cities:
            self.patterns.append(('City', city, re.compile(r'\b' + city + r'\b', re.IGNORECASE), 'city'))

        # Loading counties
        filepath = 'Selo.csv'
        counties = load_unique_counties(filepath)
        for county in counties:
            self.patterns.append(('County', county, re.compile(r'\b' + county + r'\b', re.IGNORECASE), 'county'))

    def analyze_text_file(self, filepath):
        found_cities = []
        found_counties = []
        with open(filepath, 'r') as file:
            text = file.read()
            for type_, name, pattern, _ in self.patterns:
                for match in pattern.finditer(text):
                    position = match.span()
                    formatted_name = name.capitalize()
                    if type_ == 'City':
                        found_cities.append((formatted_name, position))
                    else:
                        found_counties.append((formatted_name, position))

        print('\nЗнайдені міста:')
        for city, position in found_cities:
            print(f"{city} на позиції {position}")

        print('\nЗнайдені села:')
        for county, position in found_counties:
            print(f"{county} на позиції {position}")


if "__main__" == __name__:
    tp = TextProcessor()
    tp.analyze_text_file('input_cities.txt')