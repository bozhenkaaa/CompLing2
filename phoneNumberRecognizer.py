import re
from collections import defaultdict

class PhoneNumberRecognizer:
    def __init__(self):
        self.patterns = {
            'США': r'\+1\s?\(?\d{3}\)?\s?\d{3}[-.\s]?\d{4}',
            'Україна': r'\+380\s?\(?\d{2}\)?\s?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}',
            'Німеччина': r'\+49\s?\d{1,4}\s?\d{3,8}',
            'Великобританія': r'\+44\s?\d{3,4}\s?\d{3,4}\s?\d{3,4}',
            'Франція': r'\+33\s?\d{1}\s?\d{8}',
            'Польща': r'\+48\s?\d{2,3}\s?\d{3}[-.\s]?\d{4}',
            'Південна Корея': r'\+82\s?\d{1,4}\s?\d{3,4}\s?\d{4}',
            'Бразилія': r'\+55\s?\d{2}\s?\d{4,5}[-.\s]?\d{4}',
            'Індія': r'\+91\s?\d{5}\s?\d{5}',
            'Японія': r'\+81\s?\d{1,4}\s?\d{4}\s?\d{4}',
            'Австралія': r'\+61\s?\d{1,4}\s?\d{4}\s?\d{4}',
            'Канада': r'\+1\s?\(?\d{3}\)?\s?\d{3}[-.\s]?\d{4}',
            'Іспанія': r'\+34\s?\d{2,3}\s?\d{3}\s?\d{3,4}',
            'Італія': r'\+39\s?\d{2,4}\s?\d{6,8}'
        }

    def read_text_from_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Файл {filepath} не знайдено.")
            return None

    def process_text(self, text):
        recognized_phone_numbers = defaultdict(list)
        for country, pattern in self.patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                recognized_phone_numbers[country].extend(matches)
        return recognized_phone_numbers

    def recognize(self, filepath):
        text = self.read_text_from_file(filepath)
        if text is not None:
            recognized_phone_numbers = self.process_text(text)
            for country, numbers in recognized_phone_numbers.items():
                print(f"Знайдено номери телефонів для {country}: {', '.join(numbers)}")


recognizer = PhoneNumberRecognizer()
recognizer.recognize('input_phone_numbers.txt')