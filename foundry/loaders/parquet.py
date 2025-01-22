import pyarrow.parquet as pq
from .base import DataLoader

class ParquetDataLoader(DataLoader):
    def supports_format(self, file_path):
        return file_path.suffix.lower() == '.parquet'
        
    def load(self, file_path, schema, split=None):
        df = pq.read_table(file_path).to_pandas()
        return (
            df[self.get_keys(schema, "input")],
            df[self.get_keys(schema, "target")]
        ) 