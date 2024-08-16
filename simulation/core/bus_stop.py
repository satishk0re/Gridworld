from typing import List
from simulation.core.traveler import Traveler
from simulation.util.infection_model import get_infection_probability
import random


class BusStop:
    def __init__(self, stop_id):
        self.stop_id = stop_id
        self.queue: List[Traveler] = []

    def add_traveler(self, traveler: Traveler):
        """
        Adds a traveler to the bus stop queue.
        :param traveler: The traveler to be added to th queue.
        """
        self.queue.append(traveler)

    def remove_travelers(self, number: int) -> List[Traveler]:
        """
        Removes the specific number of travelers from the bus stop queue.
        :param number: The number of travellers to remove from the queue.
        :return: List[Traveler]: The list of removed travelers.
        """
        removed_travelers = self.queue[:number]
        self.queue = self.queue[number:]
        return removed_travelers

    def spread_infection(self, probability_matrix: List[List[float]], age_groups: List[int]):
        """
        Spreads infection among travelers at the bus stop.
        :param probability_matrix: Matrix with infection probabilities.
        :param age_groups: List defining age groups for probability lookup.
        """
        infected_travelers = [traveler for traveler in self.queue if traveler.is_infected()]
        susceptible_travelers = [traveler for traveler in self.queue if not traveler.is_infected()]

        for traveler in susceptible_travelers:
            if not traveler.is_recovered():
                contacts = random.sample(infected_travelers, min(len(infected_travelers), 5))
                for contact in contacts:
                    infection_probability = get_infection_probability(traveler.age, contact.wears_mask,
                                                                      probability_matrix, age_groups,
                                                                      location='bus_stop')
                    if random.random() < infection_probability:
                        traveler.infect()
                        break
