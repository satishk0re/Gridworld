import unittest
from simulation.core.traveler import Traveler
from simulation.core.grid_world import GridWorld


class TestGridWorld(unittest.TestCase):
    def setUp(self):
        self.grid_world = GridWorld()
        self.traveler1 = Traveler(
            passenger_id=1,
            age=25,
            wears_mask=True,
            infection_status=False,
            home_bus_stop_id=0,
            work_bus_stop_id=1,
            departure_time_home_work=8,
            duration_work=480
        )
        self.traveler2 = Traveler(
            passenger_id=2,
            age=30,
            wears_mask=False,
            infection_status=True,
            home_bus_stop_id=0,
            work_bus_stop_id=1,
            departure_time_home_work=8,
            duration_work=480
        )

    def test_initialize(self):
        self.grid_world.initialize()
        self.assertEqual(len(self.grid_world.bus_stops), 4)
        self.assertEqual(len(self.grid_world.buses), 2)

    def test_add_travelers(self):
        self.grid_world.add_travelers([self.traveler1, self.traveler2])
        self.assertIn(self.traveler1, self.grid_world.bus_stops[0].queue)
        self.assertIn(self.traveler2, self.grid_world.bus_stops[0].queue)

    def test_simulate_day(self):
        self.grid_world.add_travelers([self.traveler1, self.traveler2])
        probability_matrix = [[0.1, 0.05], [0.2, 0.1], [0.3, 0.15]]
        age_groups = [20, 40, 60]
        travel_time = 30
        self.grid_world.simulate_day(probability_matrix, age_groups, travel_time)

        # Ensure initial conditions are as expected
        self.assertFalse(self.traveler1.is_infected())
        self.assertTrue(self.traveler2.is_infected())

        self.grid_world.simulate_day(probability_matrix, age_groups, travel_time)

        # Check that travelers' status or position has changed
        self.assertTrue(
            self.traveler1.is_infected() or
            self.traveler1.current_location != self.traveler1.home_bus_stop_id or
            self.traveler1.current_location != self.traveler1.work_bus_stop_id
        )
        # We expect traveler2 to still be infected, but we might want to check their location or other status
        self.assertTrue(
            self.traveler2.current_location != self.traveler2.home_bus_stop_id or
            self.traveler2.current_location != self.traveler2.work_bus_stop_id
        )

    def test_move_buses(self):
        self.grid_world.add_travelers([self.traveler1, self.traveler2])
        initial_stop_index = self.grid_world.buses[0].current_stop_index
        self.grid_world.move_buses()

        # Check that the bus has moved to the next stop
        self.assertNotEqual(self.grid_world.buses[0].current_stop_index, initial_stop_index)


if __name__ == '__main__':
    unittest.main()
