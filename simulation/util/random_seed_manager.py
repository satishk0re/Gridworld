import random
import numpy as np


def set_random_seed(seed: int):
    """
    Sets the random seed for reproducibility.
    :param seed: The random seed value
    """
    random.seed(seed)
    np.random.seed(seed)
