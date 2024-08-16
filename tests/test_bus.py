import unittest
from simulation.core.traveler import Traveler
from simulation.core.bus_stop import BusStop
from simulation.core.bus import Bus


class TestBus(unittest.TestCase):
    def setUp(self):
        self.bus = Bus(capacity=20, route=[0, 1, 2, 3])
        self.bus_stop = BusStop(1)
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

    def test_add_traveler(self):
        self.bus.add_passenger(self.traveler1)
        self.assertIn(self.traveler1, self.bus.passengers)

    def test_remove_passengers(self):
        self.bus.add_passenger(self.traveler1)
        self.bus.add_passenger(self.traveler2)
        removed_passengers = self.bus.remove_passengers(self.traveler1.work_bus_stop_id)
        self.assertIn(self.traveler1, removed_passengers)
        self.assertNotIn(self.traveler1, self.bus.passengers)

    def test_move_to_next_stop(self):
        bus_stops = [BusStop(i) for i in range(4)]
        bus_stops[1].add_traveler(self.traveler1)
        self.bus.move_to_next_stop(bus_stops)
        self.assertIn(self.traveler1, self.bus.passengers)
        self.assertNotIn(self.traveler1, bus_stops[1].queue)

    def test_spread_infection(self):
        self.bus.add_passenger(self.traveler1)
        self.bus.add_passenger(self.traveler2)
        probability_matrix = [[0.1, 0.05], [0.2, 0.1], [0.3, 0.15]]
        age_groups = [20, 40, 60]
        self.bus.spread_infection(probability_matrix, age_groups)
        self.assertTrue(self.traveler1.is_infected())


if __name__ == '__main__':
    unittest.main()
