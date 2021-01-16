import json
import logging
import sqlite3
from os import path


class DeputyDetailsLoader:
    def __init__(self, deputy_file_path: str, database_file: str):
        self.deputy_file_path_ = deputy_file_path
        self.database_file_ = database_file

    def load_to_database(self):
        try:
            updated_deputies = self.__parse_deputies()
            logging.info(f'Deputy details from file {path.basename(self.deputy_file_path_)} parsed. '
                         f'Updated deputies count: {updated_deputies}')
        except Exception as e:
            logging.error(f'Error while parsing deputies file: {self.deputy_file_path_}')
            logging.debug(e, exc_info=True)

    def __parse_deputies(self):
        updated_deputies = 0
        with open(self.deputy_file_path_) as file:
            deputies = json.load(file)
            with sqlite3.connect(self.database_file_) as database:
                for deputy in deputies:
                    if self.__update_deputy(database, deputy):
                        updated_deputies += 1
                database.commit()
        return updated_deputies

    def __update_deputy(self, database, deputy):
        cur = database.cursor()
        deputy_id = self.__get_deputy_id(cur, deputy)
        if deputy_id is None:
            return False
        if 'club' in deputy:
            cur.execute('UPDATE deputy SET party=?, district_number=? WHERE id=?',
                        (deputy['club'], deputy['discritNum'], deputy_id))
        else:
            cur.execute('UPDATE deputy SET district_number=? WHERE id=?',
                        (deputy['discritNum'], deputy_id))
        return True

    def __get_deputy_id(self, cur, deputy):
        cur.execute('SELECT id FROM deputy WHERE name=?', (deputy['firstLastName'],))
        row = cur.fetchone()
        if row is not None:
            return row[0]

        first_name = deputy['firstName']
        last_name = deputy['lastName']
        cur.execute(f"SELECT id FROM deputy "
                    f"WHERE name LIKE '{first_name}%' "
                    f"AND name LIKE '%{last_name}'")
        rows = cur.fetchall()
        if rows is None or len(rows) == 0:
            return None
        if len(rows) > 1:
            raise Exception('Found more than one deputy matching first and last name')

        return rows[0][0]
