import pickle
import pandas as pd

class Pipeline:
    def __init__(self, version: str = 'LogisticRegression'):
        self.model_path = f'storage/models/artifacts/{version}.pkl'
        self.preprocessor_path = f'storage/models/artifacts/preprocessor.pkl'
        
        with open(self.preprocessor_path, 'rb') as f:
            self.preprocessor = pickle.load(f)
        
        self.model = None
        self.select_model(version)

    def select_model(self, version: str):
        self.model_path = f'storage/models/artifacts/{version}.pkl'
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)

    def predict(self, input_data: dict) -> bool:
        df = pd.DataFrame([input_data])

        transformed_data = self.preprocessor.transform(df)

        prediction = self.model.predict(transformed_data)[0]

        return bool(prediction)
