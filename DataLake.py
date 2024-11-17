import models

class DataLake:
    def __init__(self):
        conn = models.get_db_connection()
        cursor = conn.cursor()
        self.cursor = cursor

    def get_data(self, data_set):
        self.cursor.execute('SELECT * FROM ?', (data_set,))
        rows = self.cursor.fetchall()
        return rows

    def get_data_filtered(self, data_set, timestamp):
        query = f'SELECT * FROM {data_set} WHERE timestamp >= ?'
        self.cursor.execute(query, (timestamp,))
        rows = self.cursor.fetchall()
        return rows
