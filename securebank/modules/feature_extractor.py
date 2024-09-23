import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline as SklearnPipeline

class Feature_Extractor:
    
    def __init__(self):
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), ['amt', 'merch_lat', 'merch_long']), 
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['category', 'merchant'])  
            ])
        
        self.pipeline = SklearnPipeline(steps=[
            ('preprocessor', self.preprocessor)
        ])
        
    def extract(self, training_dataset_filename: str, testing_dataset_filename: str):
        training_dataset = pd.read_parquet(training_dataset_filename)
        testing_dataset = pd.read_parquet(testing_dataset_filename)
        return training_dataset, testing_dataset
    
    def transform(self, training_dataset: pd.DataFrame, testing_dataset: pd.DataFrame):
        features_to_keep = ['amt', 'category', 'merchant', 'merch_lat', 'merch_long', 'is_fraud']
        
        training_data = training_dataset[features_to_keep].copy()
        testing_data = testing_dataset[features_to_keep].copy()
        
        training_data_transformed = self.pipeline.fit_transform(training_data.drop(columns=['is_fraud']))
        testing_data_transformed = self.pipeline.transform(testing_data.drop(columns=['is_fraud']))

        transformed_columns = (
            self.pipeline.named_steps['preprocessor'].transformers_[0][2] + 
            self.pipeline.named_steps['preprocessor'].transformers_[1][1].get_feature_names_out().tolist()
        )

        training_data_transformed_df = pd.DataFrame(training_data_transformed, columns=transformed_columns)
        testing_data_transformed_df = pd.DataFrame(testing_data_transformed, columns=transformed_columns)
        
        training_data_transformed_df['is_fraud'] = training_data['is_fraud'].values
        testing_data_transformed_df['is_fraud'] = testing_data['is_fraud'].values
        
        training_data_transformed_df.to_parquet('storage/dataset/train_data.parquet')
        testing_data_transformed_df.to_parquet('storage/dataset/test_data.parquet')
        
        with open('storage/models/artifacts/preprocessor.pkl', 'wb') as f:
            pickle.dump(self.pipeline.named_steps['preprocessor'], f)
        
        return training_data_transformed_df, testing_data_transformed_df
    
    def describe(self, *args, **kwargs):
        description = {
            'version': kwargs.get('version', '1.0'),
            'storage': kwargs.get('storage', '/default/path'),
            'description': {
                'columns': 'Transformed Data (scaling + one-hot encoded)',
                'num_records': len(args[0])
            }
        }
        return description
