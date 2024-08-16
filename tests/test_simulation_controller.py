import unittest
from unittest.mock import patch
from simulation.control.simulation_controller import SimulationController
from simulation.core.grid_world import GridWorld


class TestSimulatorController(unittest.TestCase):
    def setUp(self):
        self.passenger_file = 'data/passengers.csv'
        self.probability_file = 'data/probability.csv'
        self.seed = 42

    @patch('simulation.control.simulation_controller.PassengerDataLoader.load_passenger_data')
    @patch('simulation.control.simulation_controller.ProbabilityDataLoader.load_probability_data')
    def test_initialization(self, mock_load_probability_data, mock_load_passenger_data):
        mock_load_passenger_data.return_value = []
        mock_load_probability_data.return_value = []

        controller = SimulationController(self.passenger_file, self.probability_file, self.seed)
        mock_load_passenger_data.assert_called_once_with(self.passenger_file)
        mock_load_probability_data.assert_called_once_with(self.probability_file)

    @patch.object(GridWorld, 'save_results')
    @patch('simulation.control.simulation_controller.YearlySimulator.simulate_year')
    def test_run(self, mock_simulate_year, mock_save_results):
        mock_simulate_year.return_value = None
        mock_save_results.return_value = None

        controller = SimulationController(self.passenger_file, self.probability_file, self.seed)

        days = 365
        travel_time = 30
        output_file = 'results/test_simulation_results.csv'

        controller.run(days, travel_time, output_file)

        mock_simulate_year.assert_called_once_with(days)
        mock_save_results.assert_called_once_with(output_file)

    @patch('simulation.util.random_seed_manager.set_random_seed')
    def test_set_random_seed(self, mock_set_random_seed):
        SimulationController(self.passenger_file, self.probability_file, self.seed)
        mock_set_random_seed.assert_called_once_with(self.seed)


if __name__ == '__main__':
    unittest.main()
