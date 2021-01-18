import logging
import sqlite3
from typing import List, Tuple


class InterpellationRegionSolver:

    def __init__(self, database_path: str):
        self.database_path_ = database_path

    def perform_settle_correlation(self):
        logging.info('Perform finding correlation between interpellations and settles')

        with sqlite3.connect(self.database_path_) as database:
            cur = database.cursor()

            interpellations = cur.execute('SELECT id, processed_content FROM interpellation').fetchall()
            settles = cur.execute('SELECT id, name, county_id, voivodeship_id FROM settle').fetchall()

            interpellations_checked = 0
            for inter in interpellations:
                (inter_id, content) = (inter[0], inter[1])
                proper_names = content.split(',')

                for name in proper_names:
                    # settle_id, settle_name = self.find_settle(name, cur)
                    settle_id, _ = self.find_settle(name, settles)
                    if settle_id is not None and not self.correlationAlreadyExists(cur, settle_id, inter_id):
                        cur.execute('INSERT INTO interpellation_settles (settle_id, interpellation_id) VALUES (?,?)',
                                    (settle_id, inter_id))
                interpellations_checked += 1

                # print debug info
                if interpellations_checked % 1000 == 0:
                    logging.info('%d interpellations checked.', interpellations_checked)
            database.commit()

    def find_settle(self, name: str, settles: List[Tuple[int, str, int, int]]) -> (int, str):
        founded = [(settle_id, settle_name) for (settle_id, settle_name, _, _) in settles if
                   settle_name.lower() == name.lower()]

        if not founded:
            return None, None  # settle does not exists
        if len(founded) > 1:
            return None, None  # settle is ambigious

        s_id = founded[0][0]
        s_name = founded[0][1]
        return s_id, s_name

    #
    # def find_settle(self, settle_name: str, cur: sqlite3.Cursor) -> (int, str):
    #     founded = cur.execute('SELECT id, name, county_id, voivodeship_id FROM settle WHERE lower(name) = lower(?)',
    #                           (settle_name,)).fetchall()
    #     if not founded:
    #         return None, None  # settle does not exists
    #     if len(founded) > 1:
    #         return None, None  # settle is ambigious
    #
    #     s_id = founded[0][0]
    #     s_name = founded[0][1]
    #     return s_id, s_name

    def correlationAlreadyExists(self, cur: sqlite3.Cursor, settle_id: int, interpellation_id: int):
        founded = cur.execute('SELECT settle_id, interpellation_id FROM interpellation_settles '
                              'WHERE settle_id = ? AND interpellation_id = ?',
                              (settle_id, interpellation_id)).fetchall()
        return bool(founded)
