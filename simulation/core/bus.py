from typing import List
from simulation.core.traveler import Traveler
from simulation.core.bus_stop import BusStop
from simulation.util.infection_model import get_infection_probability
import random


class Bus(BusStop):
    def __init__(self, capacity: int, route: List[int]):
        super().__init__(stop_id=0)  # Initialize with dummy stop_id
        self.capacity = capacity
        self.passengers: List[Traveler] = []
        self.route = route  # List of bus stop IDs that the bus will visit
        self.current_stop_index = 0  # Index in the route for the current stop

    def add_passenger(self, traveler: Traveler):
        """
        Adds a traveler to the bus if there is enough capacity.
        :param traveler: The traveler to be added to the bus.
        """
        if len(self.passengers) < self.capacity:
            self.passengers.append(traveler)

    def remove_passengers(self, stop_id: int) -> List[Traveler]:
        """
        Removes a specified number of passengers from the bus.
        :param stop_id: Te number of passengers to remove rom bus.
        :return: List: The list of removed passengers.
        """
        removed_passengers = [passenger for passenger in self.passengers if passenger.work_bus_stop_id == stop_id
                              or passenger.home_bus_stop_id == stop_id]
        self.passengers = [passenger for passenger in self.passengers if passenger not in removed_passengers]
        return removed_passengers

    def move_to_next_stop(self, bus_stops: List[BusStop]):
        current_stop_id = self.route[self.current_stop_index]
        next_stop_id = self.route[(self.current_stop_index + 1) % len(self.route)]
        self.current_stop_index = (self.current_stop_index + 1) % len(self.route)

        # Passengers alight at current stop
        alighting_passengers = self.remove_passengers(current_stop_id)
        bus_stops[current_stop_id].queue.extend(alighting_passengers)

        # Passengers board at the next stop
        boarding_passengers = bus_stops[next_stop_id].remove_travelers(self.capacity - len(self.passengers))
        self.passengers.extend(boarding_passengers)

    def spread_infection(self, probability_matrix: List[List[float]], age_groups: List[int]):
        """
        Spreads infection among passengers on the bus.
        :param probability_matrix: Matrix with infection probabilities.
        :param age_groups: List defining age groups for probability matrix.
        """
        infected_passengers = [passenger for passenger in self.passengers if passenger.is_infected()]
        susceptible_passengers = [passenger for passenger in self.passengers if not passenger.is_infected()]

        for passenger in susceptible_passengers:
            if not passenger.is_recovered():
                contacts = random.sample(infected_passengers, min(len(infected_passengers), 10))
                for contact in contacts:
                    infection_probability = get_infection_probability(passenger.age, contact.wears_mask,
                                                                      probability_matrix, age_groups,
                                                                      location='bus')
                    if random.random() < infection_probability:
                        passenger.infect()
                        break
