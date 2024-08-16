import unittest
from simulation.core.traveler import Traveler


class TestTraveler(unittest.TestCase):
    def setUp(self):
        self.traveler = Traveler(
            passenger_id=1,
            age=25,
            wears_mask=True,
            infection_status=False,
            home_bus_stop_id=0,
            work_bus_stop_id=1,
            departure_time_home_work=8,  # 8 AM
            duration_work=480  # 8 hours work duration
        )

    def test_infect(self):
        self.traveler.infect()
        self.assertTrue(self.traveler.is_infected())

    def test_recover(self):
        self.traveler.infect()
        self.traveler.recover()
        self.assertTrue(self.traveler.is_recovered())

    def test_initial_test(self):
        self.assertFalse(self.traveler.is_infected())
        self.assertFalse(self.traveler.is_recovered())

    """def test_update_daily_status(self):
        # Simulate a day when the traveler travels to work and back
        self.traveler.update_daily_status(8, 30)
        self.assertTrue(self.traveler.traveling)
        self.traveler.update_daily_status(9, 30)
        self.assertFalse(self.traveler.traveling)
        self.assertTrue(self.traveler.at_work)"""

    def test_update_daily_status(self):
        # Simulate starting the journey to work at 8 AM
        self.traveler.update_daily_status(8, 30)
        self.assertTrue(self.traveler.traveling, "Traveler should be traveling at 8 AM")

        # Simulate arrival at work at 8:30 AM
        self.traveler.update_daily_status(8 + 30 // 60, 30)
        self.assertFalse(self.traveler.traveling, "Traveler should not be traveling at 8:30 AM")
        self.assertTrue(self.traveler.at_work, "Traveler should be at work at 8:30 AM")

        # Simulate starting the journey home after 8 hours of work
        self.traveler.update_daily_status(8 + 480 // 60, 30)  # 8 AM + 8 hours work = 4 PM
        self.assertTrue(self.traveler.traveling, "Traveler should be traveling home at 4 PM")

        # Simulate arrival at home at 4:30 PM
        self.traveler.update_daily_status(8 + 480 // 60 + 30 // 60, 30)
        self.assertFalse(self.traveler.traveling, "Traveler should not be traveling at 4:30 PM")
        self.assertFalse(self.traveler.at_work, "Traveler should not be at work at 4:30 PM")
        self.assertEqual(self.traveler.current_location, self.traveler.home_bus_stop_id,
                         "Traveler should be at home at 4:30 PM")


if __name__ == '__main__':
    unittest.main()
