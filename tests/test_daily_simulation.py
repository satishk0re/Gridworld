import unittest
from unittest.mock import patch
from simulation.control.daily_simulation import DailySimulator
from simulation.core.grid_world import GridWorld
from simulation.core.traveler import Traveler


class TestDailySimulation(unittest.TestCase):
    def setUp(self):
        self.grid_world = GridWorld()
        self.travelers = [
            Traveler(
                passenger_id=1,
                age=25,
                wears_mask=True,
                infection_status=False,
                home_bus_stop_id=0,
                work_bus_stop_id=1,
                departure_time_home_work=8,
                duration_work=480
            ),
            Traveler(
                passenger_id=2,
                age=30,
                wears_mask=False,
                infection_status=True,
                home_bus_stop_id=0,
                work_bus_stop_id=1,
                departure_time_home_work=8,
                duration_work=480

            )
        ]
        self.probability_matrix = [
            [0.1, 0.05],  # Age groups 41 -60
            [0., 0.1],  # Age groups 41 -60
            [0.3, 0.15],  # Age groups 41 -60
        ]
        self.age_groups = [20, 40, 60]
        self.travel_time = 30

    def test_initialization(self):
        simulator = DailySimulator(
            self.grid_world,
            self.travelers,
            self.probability_matrix,
            self.age_groups,
            self.travel_time
        )
        self.assertEqual(simulator.grid_world, self.grid_world)
        self.assertEqual(simulator.travelers, self.travelers)
        self.assertEqual(simulator.probability_matrix, self.probability_matrix)
        self.assertEqual(simulator.age_groups, self.age_groups)
        self.assertEqual(simulator.travel_time, self.travel_time)

    @patch('simulation.control.daily_simulation.DailySimulator.run')
    def test_run(self, mock_run):
        mock_run.return_value = None

        simulator = DailySimulator(
            self.grid_world,
            self.travelers,
            self.probability_matrix,
            self.age_groups,
            self.travel_time
        )

        simulator.run()

        mock_run.assert_called_once()


if __name__ == '__main__':
    unittest.main()
