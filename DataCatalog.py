class DataTag:
    def __init__(self, id, tag, dataset):
        self.id = id
        self.tag = tag
        self.dataset = dataset

    @classmethod
    def from_row(cls, row):
        # Initialize an instance from a database row (tuple)
        return cls(id=row[0], tag=row[1], dataset=row[2])

    def __repr__(self):
        return f"DataRecord(id={self.id}, tag='{self.tag}', dataset='{self.dataset}')"


class DataCatalog:
    def __init__(self, cursor):
        self.cursor = cursor

    def get_dataset_tag(self, tag):
        self.cursor.execute('SELECT * FROM DataTags WHERE tag = ?', (tag,))
        rows = self.cursor.fetchall()
        records = [DataTag.from_row(row) for row in rows]
        return records



