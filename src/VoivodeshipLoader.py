import csv
import logging
import sqlite3
from typing import List
from os import path


class RawVoivodeship:
    def __init__(self, v_id, name):
        self.id_ = v_id
        self.name_ = name


class VoivodeshipLoader:
    def __init__(self, voivodeship_file_path, database_file):
        self.voivodeship_file_path_ = voivodeship_file_path
        self.database_file_ = database_file

    def load_to_database(self):
        voivodeship_list = None
        try:
            voivodeship_list = self.__parse_voivodeships()
            logging.info('Voivodeships from file %s parsed. Voivodeships count: %d',
                         path.basename(self.voivodeship_file_path_), len(voivodeship_list))
        except Exception as e:
            logging.error('Error while parsing voivodeships file')
            logging.debug(e, exc_info=True)

        try:
            self.__save_in_database(voivodeship_list)
            logging.info('Voivodeships saved in database')
        except sqlite3.Error as e:
            logging.error('Error occurred while inserting voivodeships data to database')
            logging.debug(e, exc_info=True)

    def __parse_voivodeships(self) -> List[RawVoivodeship]:
        voivodeship_list = []
        with open(self.voivodeship_file_path_, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader, None)  # omit header
            for row in csv_reader:
                voivodeship = RawVoivodeship(v_id=row[0], name=row[4])
                voivodeship_list.append(voivodeship)

        return voivodeship_list

    def __save_in_database(self, voivodeship_list: List[RawVoivodeship]):
        with sqlite3.connect(self.database_file_) as database:
            cur = database.cursor()
            for voivodeship in voivodeship_list:
                cur.execute('INSERT INTO voivodeship(id, name) VALUES(?,?)', (voivodeship.id_, voivodeship.name_))
            database.commit()
