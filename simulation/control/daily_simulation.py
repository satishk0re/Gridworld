from typing import List
from simulation.core.grid_world import GridWorld
from simulation.core.traveler import Traveler


class DailySimulator:
    def __init__(self, grid_world: GridWorld, travelers: List[Traveler], probability_matrix: List[List[float]],
                 age_groups: List[int], travel_time: int):
        self.grid_world = grid_world
        self.travelers = travelers
        self.probability_matrix = probability_matrix
        self.age_groups = age_groups
        self.travel_time = travel_time

    def run(self):
        """
        Run the daily simulation.
        """
        # Add travelers to the grid world
        self.grid_world.add_travelers(self.travelers)

        # Simulate a single day
        self.simulate_day()

    def simulate_day(self):
        """
        Simulates a single day in the grid world.
        """
        # Initialize the day
        for traveler in self.travelers:
            traveler.update_daily_status(current_time=0, travel_time=self.travel_time)

        # Simulate each time step
        for time_step in range(24):
            self.grid_world.move_buses()
            self.grid_world.spread_infection(self.probability_matrix, self.age_groups)

            # Update traveler statuses
            for traveler in self.travelers:
                traveler.update_daily_status(current_time=time_step, travel_time=self.travel_time)
