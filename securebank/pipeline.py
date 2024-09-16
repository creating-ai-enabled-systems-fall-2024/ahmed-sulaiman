import pickle
import os

class Pipeline:
    def __init__(self, version: str = 'LogisticRegression'):
        self.model_path = f'storage/models/artifacts/{version}.pkl'
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        self.history = []

    def predict(self, input_data: dict) -> bool:
        data = [[
            input_data['amt'], 
            input_data['category'], 
            input_data['merchant'], 
            input_data['merch_lat'], 
            input_data['merch_long']
        ]]
        prediction = self.model.predict(data)[0]

        self.history.append((input_data, prediction))
        
        return bool(prediction) 

    def select_model(self, version: str):
        self.model_path = f'storage/models/artifacts/{version}.pkl'
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)

    def get_history(self) -> dict:
        """Return the prediction history"""
        return {'history': self.history}