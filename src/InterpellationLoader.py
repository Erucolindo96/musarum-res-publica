import sqlite3
from typing import List


class RawInterpellation:
    def __init__(self, authors: List[str], date: str, content):
        self.authors_ = authors #RawInterpellation.parse_authors(authors)
        self.date_ = date.replace('\r\n', '').replace('\n', '')
        self.content_ = content.replace('\r\n', '').replace('\n', '')

    # @staticmethod
    # def parse_authors(authors: str) -> List[str]:
    #     return authors.split(sep='\n')


class InterpellationLoader:

    def __init__(self, database_path: str, parsed_interpellation_file: str):
        self.database_path_ = database_path
        self.interpellation_file_ = parsed_interpellation_file

    def load_to_database(self):
        interpellations = []
        deputies = set()
        failed = []

        with open(self.interpellation_file_, mode='r') as file:
            separated_tokens = file.read().split(sep='|')
            i = 0
            while i + 4 < len(separated_tokens):
                date = separated_tokens[i]
                deputy_names = separated_tokens[i + 1].split(sep='\n')
                content = separated_tokens[i + 4]

                # for deputy in deputy_names:
                #     if len(deputy) > 50 or deputy.islower():
                #         failed.append(i)
                #         if i == 156910:
                #             print(i)
                #             print(date, deputy_names, content)

                deputies.update(deputy_names)
                interpellations.append(RawInterpellation(deputy_names, date, content))
                i += 5

        print(failed)
        for inter in interpellations:
            print('interpellations of {} in date {}: {}'.format(inter.authors_, inter.date_, inter.content_))
    # def find_next_interpellation(self, file) -> __RawInterpellation:
