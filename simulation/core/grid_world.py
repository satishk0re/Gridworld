from typing import List
from simulation.core.bus_stop import BusStop
from simulation.core.bus import Bus
from simulation.core.traveler import Traveler
from simulation.output.output_manager import OutputManager


class GridWorld:
    def __init__(self):
        """
        Initializes the GridWorld with bus stops and buses.
        """
        self.bus_stops: List[BusStop] = [BusStop(i) for i in range(4)]
        # Example route: each bus visits stops 0, 1, 2, 3
        self.buses: List[Bus] = [Bus(20, [0, 1, 2, 4]) for _ in range(2)]
        self.travelers: List[Traveler] = []

    def initialize(self):
        """
        Reinitializes the bus stops and buses in the GridWorld.
        """
        # Initialize bus stops and buses
        self.bus_stops = [BusStop(i) for i in range(4)]
        self.buses = [Bus(20, [0, 1, 2, 4]) for _ in range(2)]

    def add_travelers(self, travelers: list[Traveler]):
        """
        Add travelers to their respective home bus stops.
        :param travelers: List of travelers to be added to the simulation.
        """
        self.travelers = travelers
        for traveler in travelers:
            home_stop = self.bus_stops[traveler.home_bus_stop_id]
            home_stop.add_traveler(traveler)

    def simulate_day(self, probability_matrix: List[List[float]], age_groups: List[int], travel_time: int):
        """
        Simulates a single day in the grid world.
        :param probability_matrix: Matrix with infection probabilities.
        :param age_groups: List defining age groups for probability lookup.
        :param travel_time: The duration of travel between home and work.
        """
        for time_step in range(24 * 60):  # Simulate each minute of a 24-hour day
            self.move_buses()
            self.spread_infection(probability_matrix, age_groups)
            self.update_travelers_status(time_step, travel_time)

    def spread_infection(self, probability_matrix: List[List[float]], age_groups: List[int]):
        """
        Spreads infection across all bus stops and buses.
        :param probability_matrix: Matrix with infection probabilities.
        :param age_groups: List defining age groups for probability lookup.
        """
        for bus_stop in self.bus_stops:
            bus_stop.spread_infection(probability_matrix, age_groups)
        for bus in self.buses:
            bus.spread_infection(probability_matrix, age_groups)

    def update_travelers_status(self, current_time: int, travel_time: int):
        """
        Updates the daily status of all travelers in the simulation.
        :param current_time: The current time in the simulation.
        :param travel_time: The duration of travel between home and work.
        """
        for bus_stop in self.bus_stops:
            for traveler in bus_stop.queue:
                traveler.update_daily_status(current_time, travel_time)
        for bus in self.buses:
            for traveler in bus.passengers:
                traveler.update_daily_status(current_time, travel_time)

    def move_buses(self):
        """
        Moves buses according to their routes.
        """
        for bus in self.buses:
            bus.move_to_next_stop(self.bus_stops)

    def save_results(self, filename: str):
        """
        Saves the infection and quarantine status of all travelers to a csv file.
        :param filename: The name of the file to sav ethe results to.
        """
        OutputManager.save_results(self.travelers, filename)
