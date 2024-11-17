from keybert import KeyBERT


class DataTag:
    def __init__(self, id, tag, dataset, metadata):
        self.id = id
        self.tag = tag
        self.dataset = dataset
        self.metadata = metadata

    @classmethod
    def from_row(cls, row):
        # Initialize an instance from a database row (tuple)
        return cls(id=row[0], tag=row[1], dataset=row[2], metadata=row[3])

    def __repr__(self):
        return f"DataRecord(id={self.id}, tag='{self.tag}', dataset='{self.dataset}')"


class DataCatalog:
    def __init__(self):
        pass

    @staticmethod
    def get_dataset_tag(tag, data_lake):
        data_lake.cursor.execute('SELECT * FROM DataTags WHERE tag = ?', (tag,))
        rows = data_lake.cursor.fetchall()
        records = [DataTag.from_row(row) for row in rows]
        unique_data_sets = set([record.dataset for record in records])
        return unique_data_sets

    @staticmethod
    def get_advanced_search_datasets(search_term, data_lake):
        data_lake.cursor.execute('SELECT * FROM DataTags')
        rows = data_lake.cursor.fetchall()
        records = [DataTag.from_row(row) for row in rows]
        unique_data_sets = set([record.dataset for record in records if search_term in record.metadata.strip("[]").split()])
        return unique_data_sets

    @staticmethod
    def get_advanced_sentence_search(body, data_lake):
        model = KeyBERT('distilbert-base-nli-mean-tokens')
        keywords = model.extract_keywords(body.sentence)
        keywords_list = [item[0] for item in keywords[:min(5, len(keywords))]]
        data_lake.cursor.execute('SELECT * FROM DataTags')
        rows = data_lake.cursor.fetchall()
        records = [DataTag.from_row(row) for row in rows]
        unique_data_sets = set()
        for record in records:
            if set(keywords_list).intersection(record.metadata.strip("[]").split()) is not None:
                unique_data_sets.add(record.dataset)
        return unique_data_sets





