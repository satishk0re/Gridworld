import random
from typing import List
from simulation.core.grid_world import GridWorld
from simulation.core.traveler import Traveler
from simulation.control.daily_simulation import DailySimulator


class YearlySimulator:
    def __init__(self, grid_world: GridWorld, travelers: List[Traveler], probability_matrix: List[List[float]],
                 age_groups: List[int], travel_time: int):
        self.grid_world = grid_world
        self.travelers = travelers
        self.probability_matrix = probability_matrix
        self.age_groups = age_groups
        self.travel_time = travel_time

    def simulate_year(self, days: int):
        """
        Simulates a full year (multiple days) in the grid world.
        :param: days: Number days to simulate.
        """
        daily_simulator = DailySimulator(self.grid_world, self.probability_matrix, self.age_groups, self.travel_time)
        self.grid_world.add_travelers(self.travelers)

        for day in range(days):
            daily_simulator.simulate_day()
            self.update_quarantine_and_recovery()
            self.handle_new_infections()

    def update_quarantine_and_recovery(self):
        """
        Updates the quarantine and recovery status of all travelers.
        """
        for traveler in self.travelers:
            if traveler.is_infected():
                # Traveler is infected, check if they need to be quarantined
                if traveler.quarantine_days > 0:
                    traveler.quarantine_days -= 1
                else:
                    traveler.recover()  # Automatically recover after quarantine period
            elif traveler.quarantine_days > 0:
                # Traveler is already in quarantine, decrement the days
                traveler.quarantine_days -= 1
            elif traveler.quarantine_days == 0 and traveler.quarantined:
                # Traveler is out of quarantine, set as recovered
                traveler.recovered = True
                traveler.quarantined = False

    def handle_new_infections(self):
        """
        Handle new infections at the end of each day.
        """
        for traveler in self.travelers:
            if traveler.is_infected() and not traveler.quarantined:
                if random.random() < 0.4:  # 40% of infected travelers quarantine
                    traveler.quarantined = True
                    traveler.quarantine_days = 7  # Quarantine for 7 days
                else:
                    traveler.quarantine_days = 14  # Not quarantining, will recover in 14 days
