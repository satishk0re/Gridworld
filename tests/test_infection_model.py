import unittest
from simulation.util.infection_model import get_infection_probability
from simulation.core.traveler import Traveler


class TestInfectionModel(unittest.TestCase):
    def setUp(self):
        self.probability_matrix = [
            [0.1, 0.05],  # Age groups 41 -60
            [0., 0.1],  # Age groups 41 -60
            [0.3, 0.15]  # Age groups 41 -60
        ]
        self.age_groups = [20, 40, 60]
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

    def test_get_infection_probability(self):
        probability = get_infection_probability(
            age=self.traveler1.age,
            wears_mask=self.traveler2.wears_mask,
            probability_matrix=self.probability_matrix,
            age_groups=self.age_groups
        )
        self.assertEqual(probability, 0.2)

    def test_apply_infection(self):
        initial_infection_status = self.traveler1.is_infected()
        infection_probability = get_infection_probability(
            age=self.traveler1.age,
            wears_mask=self.traveler2.wears_mask,
            probability_matrix=self.probability_matrix,
            age_groups=self.age_groups
        )
        if infection_probability > 0.15:  # Assuming a threshold for infection to apply
            self.traveler1.infect()
        final_infected_status = self.traveler1.is_infected()
        self.assertNotEqual(initial_infection_status, final_infected_status)


if __name__ == '__main__':
    unittest.main()
