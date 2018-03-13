# coding=utf-8
import sqlite3


class WaterAlarmSql:
    """custom SQL handler for the purpose of water alarm project"""
    def __init__(self, path):
        __name = "[water_alarm_sql __init__]"
        self.conn = sqlite3.connect(path)
        with self.conn:
            print(__name, 'Opened database successfully')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS station_status(
                station_id    INT PRIMARY KEY,
                last_date     TEXT,
                alarm1        INT,
                alarm2        INT);''')
            print(__name, 'Table created successfully')
            self.conn.commit()

    def show_table(self):
        __name = '[show_table]'
        with self.conn:
            cursor = self.conn.execute("SELECT station_id, last_date, alarm1, alarm2 from station_status")
            for row in cursor:
                print(row)

    def replace_row(self, id_m, time_m, alarm1_m, alarm2_m):
        __name = '[replace_row]'
        with self.conn:
            self.conn.execute('''REPLACE INTO station_status
                            VALUES (?, ?, ?, ?);''', (id_m, time_m, alarm1_m, alarm2_m))
            self.conn.commit()

    def get_data(self, id_m):
        __name = '[get_data]'
        with self.conn:
            cursor = self.conn.execute("SELECT station_id, last_date, alarm1, alarm2 from station_status")
            data = []
            for row in cursor:
                data.append(row)
        return data
