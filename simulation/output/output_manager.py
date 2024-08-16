import csv
from typing import List
from simulation.core.traveler import Traveler


class OutputManager:
    @staticmethod
    def save_results(travelers: List[Traveler], filename: str):
        """
        Saves the infection and quarantine status of all travelers to a csv file.
        :param travelers: List of travelers to save.
        :param filename: The name of the file to save the results to.
        """
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['passenger_id', 'infected', 'recovered', 'quarantined', 'quarantine_days']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for traveler in travelers:
                writer.writerow({
                    'passenger_id': traveler.passenger_id,
                    'infected': traveler.is_infected(),
                    'recovered': traveler.is_recovered(),
                    'quarantined': traveler.quarantined,
                    'quarantine_days': traveler.quarantine_days
                })
