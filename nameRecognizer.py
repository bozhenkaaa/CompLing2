import re


def load_unique_names(filepath):
    names = set()
    with open(filepath, 'r') as file:
        for line in file:
            name = line.strip()
            if name:  # Check if name is not empty
                names.add(name)
    return list(names)

class NameProcessor:
    def __init__(self):
        self.patterns = []

        filepath = 'names.csv'
        names = load_unique_names(filepath)
        for name in names:
            capitalized_name = name.capitalize()
            self.patterns.append(('Name',
                                  capitalized_name,
                                  re.compile(r'\b' + capitalized_name + r'\b', re.IGNORECASE)))
            genitive = re.escape(self.to_genitive_case(capitalized_name))
            self.patterns.append(
                ('Genitive', genitive, re.compile(r'(?:^|\s|(?<=\W))' + genitive + r'(?=\s|,|$|\W)', re.IGNORECASE)))

            instrumental = re.escape(self.to_instrumental_case(capitalized_name))
            self.patterns.append(('Instrumental', instrumental,
                                  re.compile(r'(?:^|\s|(?<=\W))' + instrumental + r'(?=\s|,|$|\W)', re.IGNORECASE)))

    @staticmethod
    def to_genitive_case(name):
        # Check last character of name to decide suffix
        if name and name[-1].lower() in ['а', 'я']:
            return name[:-1] + 'и'
        else:
            return name[:-1] + 'а'

    @staticmethod
    def to_instrumental_case(name):
        if name and name[-1].lower() in ['а', 'я']:
            return name[:-1] + 'ою'
        else:
            return name[:-1] + 'ом'
    def analyze_text_file(self, filepath):
        found_names = []
        with open(filepath, 'r') as file:
            text = file.read()
            for type_, name, pattern in self.patterns:
                if re.search(pattern, text):
                    found_names.append(name)

        print('Found Names:')
        for name in found_names:
            print(name)


np = NameProcessor()
np.analyze_text_file('input_names.txt')