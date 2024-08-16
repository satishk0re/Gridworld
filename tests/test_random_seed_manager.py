import unittest
import random
import numpy as np
from simulation.util.random_seed_manager import set_random_seed


class TestRandomSeedManager(unittest.TestCase):
    def test_set_random_seed(self):
        seed = 42
        set_random_seed(seed)

        # Check if the seed is set for the random library
        random_value_1 = random.random()
        random_value_2 = random.random()
        set_random_seed(seed)
        self.assertEqual(random.random(), random_value_1)
        self.assertEqual(random.random(), random_value_2)

        # Check if the seed is set for numpy
        np_random_value_1 = np.random.rand()
        np_random_value_2 = np.random.rand()
        set_random_seed(seed)
        self.assertEqual(np.random.rand(), np_random_value_1)
        self.assertEqual(np.random.rand(), np_random_value_2)


if __name__ == '__main__':
    unittest.main()
