import pandas as pd
from sklearn.model_selection import train_test_split

class Dataset_Designer:
    
    def extract(self, raw_dataset_filename: str):
        raw_dataset = pd.read_parquet(raw_dataset_filename)
        return raw_dataset
    
    def sample(self, raw_dataset: pd.DataFrame):
        train_data, test_data = train_test_split(raw_dataset, test_size=0.2, random_state=42)
        return [train_data, test_data]
    
    def describe(self, *args, **kwargs):
        description = {
            'version': kwargs.get('version', '1.0'),
            'storage': kwargs.get('storage', '/default/path'),
            'description': {
                'columns': args[0].columns.tolist(),
                'num_records': len(args[0])
            }
        }
        return description
    
    def load(self, partitioned_data: list, output_filenames: list):
        for df, filename in zip(partitioned_data, output_filenames):
            df.to_parquet(filename)