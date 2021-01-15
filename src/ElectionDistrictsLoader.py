import csv
import logging
import sqlite3
from typing import List


class RawElectionDistrict:
    def __init__(self, number: int, name: str, counties: List[str]):
        self.number_ = number
        self.name_ = name
        self.counties_ = counties


class ElectionDistrictsLoader:
    def __init__(self, districts_file_path: str, database_file: str):
        self.districts_file_path_ = districts_file_path
        self.database_file_ = database_file
        self.districts_: List[RawElectionDistrict] = []

    def load(self):
        try:
            self.districts_ = self.__parse_districts()
            logging.info('Election districts from file %s parsed. Election districts count: %d',
                         self.districts_file_path_, len(self.districts_))
        except Exception as e:
            logging.error('Error while parsing districts file: %s', self.districts_file_path_)
            logging.debug(e, exc_info=True)

    def save_to_database(self):
        try:
            saved_in_database = self.__save_districts()
            logging.info('Election districts saved in database: %d', saved_in_database)
        except sqlite3.Error as e:
            logging.error('Error occurred while inserting districts data from file %s to database',
                          self.districts_file_path_)
            logging.debug(e, exc_info=True)

    def get_county_to_district_map(self):
        map = dict()
        for district in self.districts_:
            for county in district.counties_:
                map[county] = district.number_

        return map

    def __parse_districts(self) -> List[RawElectionDistrict]:
        districts_list = []
        with open(self.districts_file_path_, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                district = RawElectionDistrict(int(row[0]), row[1], row[2].split(', '))
                districts_list.append(district)

        return districts_list

    def __save_districts(self) -> int:
        saved_num = 0
        with sqlite3.connect(self.database_file_) as database:
            cur = database.cursor()
            for district in self.districts_:
                cur.execute(
                    f'SELECT district_number name FROM election_district WHERE district_number = {district.number_}'
                )
                rows = cur.fetchall()

                # omit if election_district already exists in database
                if not rows:
                    cur.execute(
                        'INSERT INTO election_district(district_number, name) VALUES(?,?)',
                        (district.number_, district.name_)
                    )
                    saved_num += 1
            database.commit()
        return saved_num
