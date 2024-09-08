import pandas as pd

class Feature_Extractor:
    
    def extract(self, training_dataset_filename: str, testing_dataset_filename: str):
        training_dataset = pd.read_parquet(training_dataset_filename)
        testing_dataset = pd.read_parquet(testing_dataset_filename)
        return training_dataset, testing_dataset
    
    def transform(self, training_dataset: pd.DataFrame, testing_dataset: pd.DataFrame):
        features_to_keep = ['amt', 'category', 'merchant', 'merch_lat', 'merch_long', 'is_fraud']
        training_data = training_dataset[features_to_keep]
        testing_data = testing_dataset[features_to_keep]
        return [training_data, testing_data]
    
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
