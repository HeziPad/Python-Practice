# coding=utf-8
import sqlite3
import datetime

class water_alarm_sql():
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        with self.conn:
            print('Opened database successfully')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS station_status(
                station_id    INT PRIMARY KEY,
                last_date     TEXT,
                alarm1        INT,
                alarm2        INT);''')
            print('Table created successfully')
            self.conn.commit()

    def show_table(self):
        with self.conn:
            cursor = self.conn.execute("SELECT station_id, last_date, alarm1, alarm2 from station_status")
            for row in cursor:
                print(row)

    def replace_row(self, id_m, time_m, alarm1_m, alarm2_m):
        with self.conn:
            self.conn.execute('''REPLACE INTO station_status
                            VALUES (?, ?, ?, ?);''', (id_m, time_m, alarm1_m, alarm2_m))
            self.conn.commit()

    def get_data(self, id_m):
        with self.conn:
            cursor = self.conn.execute("SELECT station_id, last_date, alarm1, alarm2 from station_status")
            data = []
            for row in cursor:
                data.append(row)
        return data