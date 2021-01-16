import sqlite3
import logging
import re
from typing import List, Set
from os import path


class RawInterpellation:
    def __init__(self, authors: List[str], date: str, content):
        self.authors_ = authors
        self.date_ = date.replace('\r\n', '').replace('\n', '')
        self.content_ = content.replace('\r\n', '').replace('\n', '')


def to_sqlite_date(raw_date: str):
    match = re.search(r'(\d\d)-(\d\d)-(\d\d\d\d)', raw_date)
    if match is None:
        raise Exception(f'Could not parse interpellation date: {raw_date}')
    day = match.group(1)
    month = match.group(2)
    year = match.group(3)
    return f'{year}-{month}-{day}'


class InterpellationLoader:

    def __init__(self, database_path: str, parsed_interpellation_file: str):
        self.database_path_ = database_path
        self.interpellation_file_ = parsed_interpellation_file

    def load_to_database(self):
        interpellations = None
        deputies = None
        try:
            interpellations, deputies = self.__parse_file()
            logging.info('Interpellations from file %s parsed. Interpellations count: %d, deputies count: %d',
                         path.basename(self.interpellation_file_), len(interpellations), len(deputies))
        except Exception as e:
            logging.error('Error while parsing interpellation file')
            logging.debug(e, exc_info=True)

        try:
            self.__save_to_database(interpellations, deputies)
            logging.info('Interpellations saved in database')
        except sqlite3.Error as e:
            logging.error('Error occurred while inserting data to database')
            logging.debug(e, exc_info=True)

    def __parse_file(self) -> (List, Set):
        interpellations = []
        deputies = set()
        # failed = []
        with open(self.interpellation_file_, mode='r') as file:
            separated_tokens = file.read().split(sep='|')  # values are separated by |
            i = 0
            while i + 4 < len(separated_tokens):
                date = separated_tokens[i]
                deputy_names = separated_tokens[i + 1].split(sep='\n')  # deputies names in separated lines
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
        return interpellations, deputies

    def __save_to_database(self, interpellations, deputies):
        with sqlite3.connect(self.database_path_) as database:
            cur = database.cursor()
            for deputy_name in deputies:
                cur.execute('INSERT INTO deputy(name) VALUES(?)', (deputy_name,))

            deputy_ids = {}
            cur.execute('SELECT id, name FROM deputy')
            for row in cur.fetchall():
                deputy_ids[row[1]] = row[0]

            for inter in interpellations:
                cur.execute('INSERT INTO interpellation(date, content) VALUES(?,?)',
                            (to_sqlite_date(inter.date_), inter.content_))
                inter_id = cur.lastrowid
                for inter_deputy in inter.authors_:
                    cur.execute('INSERT INTO deputy_interpellation(deputy_id, interpellation_id) VALUES(?,?)',
                                (deputy_ids[inter_deputy], inter_id))
            database.commit()
