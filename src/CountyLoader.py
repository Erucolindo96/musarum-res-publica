import csv
import logging
import sqlite3
from typing import List


class RawCounty:
    def __init__(self, c_id, voivodeship_id, name):
        self.id_ = c_id
        self.voivodeship_id = voivodeship_id
        self.name_ = name


class CountyLoader:

    def __init__(self, county_file_path, database_file, county_to_district):
        self.county_file_path_ = county_file_path
        self.database_file_ = database_file
        self.county_to_district_ = county_to_district

    def load_to_database(self):
        county_list = None
        try:
            county_list = self.__parse_counties()
            logging.info('Counties are parser. Counties count: %d',
                         len(county_list))
        except Exception as e:
            logging.error('Error while parsing county file')
            logging.debug(e, exc_info=True)

        try:
            self.__save_in_database(county_list)
            logging.info('Counties saved in database')
        except sqlite3.Error as e:
            logging.error('Error occurred while inserting counties data to database')
            logging.debug(e, exc_info=True)

    def __parse_counties(self) -> List[RawCounty]:
        county_list = []
        with open(self.county_file_path_, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            next(csv_reader, None)  # omit header
            for row in csv_reader:
                county = RawCounty(c_id=row[1], voivodeship_id=row[0], name=row[4])
                county_list.append(county)

        return county_list

    def __save_in_database(self, county_list: List[RawCounty]):
        with sqlite3.connect(self.database_file_) as database:
            cur = database.cursor()
            for county in county_list:
                district_number = self.county_to_district_[county.name_]
                cur.execute('INSERT INTO county(id, voivodeship_id, district_number, name) VALUES(?,?,?,?)',
                            (county.id_, county.voivodeship_id, district_number, county.name_))
            database.commit()
