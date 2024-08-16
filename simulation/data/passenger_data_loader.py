import pandas as pd
from typing import List
from simulation.core.traveler import Traveler


class PassengerDataLoader:
    @staticmethod
    def load_passenger_data(file_path="data/passengers.csv") -> List[Traveler]:
        df = pd.read_csv(file_path)
        travelers = []
        for _, row in df.iterrows():
            traveler = Traveler(
                passenger_id=row['passenger_id'],
                age=row['age'],
                wears_mask=row['wears_mask'],
                infection_status=row['infection_status'],
                home_bus_stop_id=row['home_bus_stop_id'],
                work_bus_stop_id=row['work_bus_stop_id'],
                departure_time_home_work=row['departure_time_home_work'],
                duration_work=row['duration_work']
            )
            travelers.append(traveler)
        return travelers
