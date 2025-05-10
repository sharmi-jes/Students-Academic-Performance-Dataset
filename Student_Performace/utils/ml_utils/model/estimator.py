import os
import sys
import pandas as pd
from Student_Performace.exception.exception import StudentException

class NetworkModel:
    def __init__(self, preprocessor, model, label_encoders: dict):
        try:
            self.preprocessor = preprocessor
            self.model = model
            self.label_encoders = label_encoders  # Dictionary: {column_name: LabelEncoder()}
        except Exception as e:
            raise StudentException(e, sys)

    def predict(self, x: pd.DataFrame):
        try:
            # Apply label encoding to all required categorical columns
            for col, encoder in self.label_encoders.items():
                if col in x.columns:
                    x[col] = encoder.transform(x[col])

            # Now apply preprocessing (e.g. imputation)
            x_transformed = self.preprocessor.transform(x)

            # Predict using the trained model
            y_hat = self.model.predict(x_transformed)
            return y_hat

        except Exception as e:
            raise StudentException(e, sys)
