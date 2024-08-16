from typing import List


def get_infection_probability(age: int, wears_mask: bool, probability_matrix: List[List[float]], age_groups: List[int],
                              location: str) -> float:
    """
    Returns the infection probability based on age, mask-wearing status, and location.
    :param age: Age of the susceptible traveler.
    :param wears_mask: Mask status of the infected traveler.
    :param probability_matrix: Matrix with infection probabilities.
    :param age_groups: List defining age groups for probability lookup.
    :param location: 'bus' or 'bus_stop' indicating the location of the interaction.
    :return: float: The calculated infection probability
    """
    for age_group in age_groups:
        if age <= age_group:
            mask_index = 1 if wears_mask else 0
            probability = probability_matrix[age_groups.index(age_group)][mask_index]
            if location == 'bus_stop':
                probability /= 2  # Lower probability at bus stops
            return probability
    return 0.0
