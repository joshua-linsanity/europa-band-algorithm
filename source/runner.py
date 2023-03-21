from band_network import *
from test_cases import get_tests
from termcolor import colored


def main():
    print("Relative age tests for Europa bands. NOTE: probabilistic sorting is still in development.")

    tests = get_tests()[0]
    for idx, test in enumerate(tests):
        # Create a band network object
        network = BandNetwork(
            bands=test['bands'],
            intersections=test['intersections']
        )

        # TODO: remove any duplicates in `bands`
        # TODO: ignore any irrelevant bands in `intersections`
        # TODO: find bands that cause cycles, return them (and their confidence levels)

        # Determine if output matches test solution
        if network.probabilistic_sort() == test['solution']:
            label = colored("PASS", "green")
        elif network.detect_cycle():
            label = colored("CYCLE", "red")
        else:
            label = colored("FAIL", "red")

        # Print results
        print(f"""TEST #{idx + 1}: {label}
            Bands: \t\t{network.get_bands()}
            Intersections: \t{network.get_intersections()}
            Description: \t{test['description']}

            Sorted: \t\t{network.probabilistic_sort()}
            Solution: \t\t{test['solution']}
            """
        )


main()
