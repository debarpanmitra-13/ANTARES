import joblib
import os
import pandas as pd


class HazardInference:

    def __init__(self):

        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )

        model_path = os.path.join(
            base_path,
            "models",
            "trained",
            "antares_rf_model.pkl"
        )

        self.model = joblib.load(model_path)

        self.feature_names = [
            "acceleration_variance",
            "gyro_variance",
            "acoustic_energy",
            "pressure_change",
            "signal_instability"
        ]


    def predict(self, features):

        input_data = pd.DataFrame(
            [features],
            columns=self.feature_names
        )

        probability = self.model.predict_proba(
            input_data
        )[0][1]

        return float(probability)
