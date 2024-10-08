import re

class EmailRecognizer:
    def __init__(self):
        self.patterns = [
            ('GMAIL', re.compile(r'\b[A-Za-z0-9._%+-]+@gmail\.com\b')),
            ('UKR', re.compile(r'\b[A-Za-z0-9._%+-]+@ukr\.net\b')),
            ('ICLOUD', re.compile(r'\b[A-Za-z0-9._%+-]+@icloud\.com\b')),
            ('YAHOO', re.compile(r'\b[A-Za-z0-9._%+-]+@yahoo\.com\b')),
            ('HOTMAIL', re.compile(r'\b[A-Za-z0-9._%+-]+@hotmail\.com\b')),
            ('OUTLOOK', re.compile(r'\b[A-Za-z0-9._%+-]+@outlook\.com\b')),
            ('YANDEX', re.compile(r'\b[A-Za-z0-9._%+-]+@yandex\.ru\b')),
            ('MAILRU', re.compile(r'\b[A-Za-z0-9._%+-]+@mail\.ru\b')),
            ('PROTONMAIL', re.compile(r'\b[A-Za-z0-9._%+-]+@protonmail\.com\b')),
            ('AOL', re.compile(r'\b[A-Za-z0-9._%+-]+@aol\.com\b')),
            ('ZOHO', re.compile(r'\b[A-Za-z0-9._%+-]+@zoho\.com\b')),
            ('GMX', re.compile(r'\b[A-Za-z0-9._%+-]+@gmx\.com\b')),
            ('TUTANOTA', re.compile(r'\b[A-Za-z0-9._%+-]+@tutanota\.com\b')),
        ]

    def read_text_from_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Файл {filepath} не знайдено.")
            return None

    def first_pass(self, text):
        matches = []
        for tag, regex in self.patterns:
            for match in regex.finditer(text):
                matches.append({
                    'text': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'tag': tag
                })

        # Сортуємо та видаляємо перекриття
        matches.sort(key=lambda x: (x['start'], -x['end']))
        non_overlapping = []
        occupied = [False] * len(text)
        for match in matches:
            if not any(occupied[match['start']:match['end']]):
                non_overlapping.append(match)
                for i in range(match['start'], match['end']):
                    occupied[i] = True

        return non_overlapping

    def recognize(self, filepath):
        text = self.read_text_from_file(filepath)
        if text is not None:
            matches = self.first_pass(text)
            for match in matches:
                print(f"{match['tag']}: {match['text']}")
                local_part, domain = match['text'].split('@')
                print(f"{match['text']} (local part: {local_part}, domain: {domain})")

recognizer = EmailRecognizer()
recognizer.recognize('input_emails.txt')