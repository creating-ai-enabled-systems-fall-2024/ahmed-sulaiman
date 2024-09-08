import pandas as pd
import json

class Raw_Data_Handler:
    
    def extract(self, customer_information_filename: str, transaction_filename: str, fraud_information_filename: str):
        customer_information = pd.read_csv(customer_information_filename)
        transaction_information = pd.read_parquet(transaction_filename)
        with open(fraud_information_filename, 'r') as f:
            fraud_information = pd.DataFrame(list(json.load(f).items()), columns=['trans_num', 'is_fraud'])
        return customer_information, transaction_information, fraud_information
    
    def transform(self, customer_information: pd.DataFrame, transaction_information: pd.DataFrame, fraud_information: pd.DataFrame):
        transaction_information = transaction_information.reset_index()  # Ensure trans_num is a column
        merged_data = transaction_information.merge(customer_information, on='customer_id', how='left')
        merged_data = merged_data.merge(fraud_information, on='trans_num', how='left')
        
        # Data cleaning steps could be included here (e.g., dealing with missing data, standardizing column names, etc.)
        merged_data.fillna(0, inplace=True)  # Example transformation
        return merged_data

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
    
    def load(self, raw_data: pd.DataFrame, output_filename: str):
        raw_data.to_parquet(output_filename)