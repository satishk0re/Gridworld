import pandas as pd
from typing import List


class ProbabilityDataLoader:
    @staticmethod
    def load_probability_data(file_path="data/probability.csv") -> List[List[float]]:
        df = pd.read_csv(file_path)
        probability_matrix = df.values.tolist()
        return probability_matrix
