import csv
import logging
import sqlite3
from typing import List
from os import path


class RawSettle:
    def __init__(self, voivodeship_id, county_id, name):
        self.voivodeship_id_ = voivodeship_id
        self.county_id_ = county_id
        self.name_ = name


class SettleLoader:
    def __init__(self, settle_file_path: str, database_file: str):
        self.settle_file_path_ = settle_file_path
        self.database_file_ = database_file

    def load_to_database(self):
        settles_list = None
        try:
            settles_list = self.__parse_settles()
            logging.info('Settles from file %s parsed. Settles count: %d', path.basename(self.settle_file_path_),
                         len(settles_list))
        except Exception as e:
            logging.error('Error while parsing settle file: %s', self.settle_file_path_)
            logging.debug(e, exc_info=True)

        try:
            saved_in_database = self.__save_in_database(settles_list)
            logging.info('Settles saved in database: %d', saved_in_database)
        except sqlite3.Error as e:
            logging.error('Error occurred while inserting settles data from file %s to database',
                          self.settle_file_path_)
            logging.debug(e, exc_info=True)

    def __parse_settles(self) -> List[RawSettle]:
        settles_list = []
        with open(self.settle_file_path_, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader, None)  # omit header
            for row in csv_reader:
                settle = RawSettle(voivodeship_id=row[0], county_id=row[1], name=row[6])
                settles_list.append(settle)

        return settles_list

    def __save_in_database(self, settles_list: List[RawSettle]) -> int:
        saved_num = 0
        with sqlite3.connect(self.database_file_) as database:
            cur = database.cursor()
            for settle in settles_list:
                cur.execute(
                    'SELECT county_id, voivodeship_id, name FROM settle'
                    ' WHERE county_id = ? AND voivodeship_id = ? AND name = ?',
                    (settle.county_id_, settle.voivodeship_id_, settle.name_))
                rows = cur.fetchall()

                # omit if settle in this county already exists in database
                if not rows:
                    cur.execute('INSERT INTO settle(county_id, voivodeship_id, name) VALUES(?,?,?)',
                                (settle.county_id_, settle.voivodeship_id_, settle.name_))
                    saved_num += 1
            database.commit()
        return saved_num
