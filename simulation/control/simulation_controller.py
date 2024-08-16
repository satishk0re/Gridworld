from typing import Optional
from simulation.core.grid_world import GridWorld
from simulation.data.passenger_data_loader import PassengerDataLoader
from simulation.data.probability_data_loader import ProbabilityDataLoader
from simulation.control.yearly_simulation import YearlySimulator
from simulation.util.random_seed_manager import set_random_seed


class SimulationController:
    def __init__(self, passenger_file: str, probability_file: str, seed: Optional[int] = None):
        self.grid_world = GridWorld()
        self.travelers = PassengerDataLoader.load_passenger_data(passenger_file)
        self.probability_matrix = ProbabilityDataLoader.load_probability_data(probability_file)
        self.age_groups = [20, 40, 60]  # Example age groups

        if seed is not None:
            set_random_seed(seed)  # Set the random seed if provided

    def run(self, days: int, travel_time: int, output_file: str):
        yearly_simulator = YearlySimulator(self.grid_world, self.travelers, self.probability_matrix, self.age_groups,
                                           travel_time)
        yearly_simulator.simulate_year(days)
        self.grid_world.save_results(output_file)
