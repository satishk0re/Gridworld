from simulation.control.simulation_controller import SimulationController


def main():
    passenger_file = 'data/passengers.csv'
    probability_file = 'data/probability.csv'
    days = 365  # Number of days to simulate
    travel_time = 30  # Example travel time in minutes
    output_file = 'results/simulation_results.csv'
    seed = 42

    controller = SimulationController(passenger_file, probability_file, seed)
    controller.run(days, travel_time, output_file)


if __name__ == '__main__':
    main()
