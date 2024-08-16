from typing import Optional


class Traveler:
    def __init__(self, passenger_id: int, age: int, wears_mask: bool, infection_status: bool, home_bus_stop_id: int,
                 work_bus_stop_id: int, departure_time_home_work: int, duration_work: int):
        self.passenger_id = passenger_id
        self.age = age
        self.wears_mask = wears_mask
        self._infection_status = infection_status
        self._recovered = False
        self.home_bus_stop_id = home_bus_stop_id
        self.work_bus_stop_id = work_bus_stop_id
        self.departure_time_home_work = departure_time_home_work
        self.duration_work = duration_work
        self._current_location = home_bus_stop_id
        self._traveling = False
        self._at_work = False
        self.quarantined = False  # Indicates if the traveler is in quarantine
        self.quarantine_days = 0  # Number of days left in quarantine

    def infect(self) -> None:
        """
        Infects the traveler if they have not already recovered from a previous infection.
        """
        if not self._recovered:
            self._infection_status = True

    def recover(self) -> None:
        """
        Marks the traveler as recovered from the infection.
        """
        self._infection_status = False
        self._recovered = True

    def is_infected(self) -> bool:
        """
        Checks if the traveler is currently infected.
        """
        return self._infection_status

    def is_recovered(self) -> bool:
        """
        Checks if traveler is recovered from the infection.
        :return: bool: True if infected, False otherwise.
        """
        return self._recovered

    @property
    def traveling(self) -> bool:
        """
        Returns whether the traveler is currently traveling.
        :return: bool: True if traveling, False otherwise.
        """
        return self._traveling

    @property
    def at_work(self) -> bool:
        """
        Returns whether the traveler is at work
        :return: bool: True if at work, False otherwise.
        """
        return self._at_work

    @at_work.setter
    def at_work(self, value: bool):
        """
        Sets the work status of the traveler.
        :param value: True if the traveler is at work, False otherwise.
        """
        self._at_work = value

    @property
    def current_location(self) -> Optional[int]:
        """
        Returns the current location of the traveler.
        :return: The current location ID of the traveler.
        """
        return self._current_location

    @current_location.setter
    def current_location(self, value: Optional[int]):
        """
        Sets the current location of the traveler.
        :return: The new location ID of the traveler.
        """
        self._current_location = value

    def start_travel_to_work(self) -> None:
        """
        Initiates the traveler's journey to work.
        """
        self._traveling = True
        self._at_work = False
        self._current_location = None  # Not at a bus stop or work

    def arrive_at_work(self) -> None:
        """
        Marks the traveler as having arrived at their workplace.
        """
        self._traveling = False
        self._at_work = True
        self._current_location = self.work_bus_stop_id

    def start_travel_to_home(self) -> None:
        """
        Initiates the traveler's journey back home.
        """
        self._traveling = True
        self._at_work = False
        self._current_location = None  # Not at a bus stop or work

    def arrive_at_home(self) -> None:
        """
        Marks the traveler as having arrived back home.
        """
        self._traveling = False
        self._current_location = self.home_bus_stop_id

    def update_daily_status(self, current_time: int, travel_time: int) -> None:
        """
        Updates the traveler's daily status based on the current time.
        This method manages transitions between home, traveling, and work states
        according to the traveler's schedule.
        :param current_time: The current time in the simulation.
        :param travel_time: The duration of travel between home and work.
        """
        # Start traveling to work at departure time
        if current_time == self.departure_time_home_work:
            self.start_travel_to_work()

        # Arrive at work after travel time has passed
        elif current_time == self.departure_time_home_work + travel_time:
            self.arrive_at_work()

        # Start traveling home after work duration is over
        elif current_time == self.departure_time_home_work + self.duration_work:
            self.start_travel_to_home()

        # Arrive home after travel time from work
        elif current_time == self.departure_time_home_work + self.duration_work + travel_time:
            self.arrive_at_home()
