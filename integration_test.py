import os
from simulation.data.passenger_data_loader import PassengerDataLoader
from simulation.data.probability_data_loader import ProbabilityDataLoader
from simulation.control.simulation_controller import SimulationController


def run_integration_test():
    passenger_file = "data/passengers.csv"
    probability_file = "data/probability.csv"
    output_file = "results/integration_test_results.csv"
    days = 365
    travel_time = 30
    seed = 42

    # Load data
    passengers = PassengerDataLoader.load_passenger_data(passenger_file)
    probability_matrix = ProbabilityDataLoader.load_probability_data(probability_file)

    # Verify data loading
    assert len(passengers) > 0, "No passengers loaded"
    assert len(probability_matrix) > 0, "Probability matrix not loaded"

    # Run simulation
    controller = SimulationController(passenger_file, probability_file, seed)
    controller.run(days, travel_time, output_file)

    # Check if output file is created
    assert os.path.exists(output_file), "Output file not created"


if __name__ == "__main__":
    run_integration_test()
    print("Integration test completed successfully.")
