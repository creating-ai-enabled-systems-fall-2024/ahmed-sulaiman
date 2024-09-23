import pandas as pd
from sklearn.model_selection import train_test_split

class Dataset_Designer:
    
    def extract(self, raw_dataset_filename: str):
        raw_dataset = pd.read_parquet(raw_dataset_filename)
        return raw_dataset
    
    def sample(self, raw_dataset: pd.DataFrame):
        customer_groups = raw_dataset.groupby('cc_num')

        unique_customers = raw_dataset['cc_num'].unique()

        train_customers, test_customers = train_test_split(unique_customers, test_size=0.2, random_state=42)

        train_data = raw_dataset[raw_dataset['cc_num'].isin(train_customers)]
        test_data = raw_dataset[raw_dataset['cc_num'].isin(test_customers)]

        return train_data, test_data
    
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
    
    def load(self, data: list, output_filenames: list):
        if len(data) != len(output_filenames):
            raise ValueError("The number of datasets and filenames must match.")
        
        for df, filename in zip(data, output_filenames):
            df.to_parquet(filename)
