import random
from band_network import *
from termcolor import colored


def run_tests():
    print("Relative age tests for Europa bands.")
    tests = get_tests()
    
    for idx, test in enumerate(tests):
        # Create a BandNetwork object
        network = BandNetwork(
            bands=test['bands'],
            intersections=test['intersections']
        )

        # Determine if output matches test solution
        if network.top_sort() == test['solution']:
            label = colored("PASS", "green")
            solved_message = network.sorted
            code = "Sorted"
        elif network.check_cycle():
            label = colored("CYCLE", "yellow")
            solved_message = f"{network.find_cycle()}"
            code = "Cycles"
        else:
            label = colored("FAIL", "red")
            solved_message = network.sorted
            code = "Sorted"

        # Print results
        print(f"""TEST #{idx + 1}: {label}
            Bands: \t\t{network.get_bands()}
            Intersections: \t{network.get_intersections()}
            Description: \t{test['description']}
            Deviation: \t\t{network.calculate_accuracy()}
            {code}: \t\t{solved_message}
            Solution: \t\t{test['solution']}
            """
        )

def get_tests():
    # Duplicates in 'bands' list will automatically be removed.
    tests = [
        {
            'bands': ['red', 'green', 'blue', 'black'],
            'intersections': [('blue', 'red'), ('blue', 'green'), ('red', 'green'), ('green', 'black')],
            'solution': ['blue', 'red', 'green', 'black'],
            'description': "2 bands per node."
        },
        {
            'bands': ['red', 'green', 'blue', 'black'], 
            'intersections': [('blue', 'red', 'pink'), ('blue', 'green', 'orange'), ('red', 'green'), ('green', 'black'), ('black', 'pink')],
            'solution': ['blue', 'red', 'green', 'black'],
            'description': "2 bands per node, but some nodes have extra unlisted band (which should be ignored)."
        },
        {
            # 'bands': ['red', 'blue', 'black', 'green', 'pink', 'red', 'black', 'pink'],
            'bands': ['red', 'blue', 'black', 'green', 'pink'],
            'intersections': [('blue', 'pink', 'red'), ('blue', 'green', 'pink'), ('red', 'green', 'pink'), ('green', 'black'), ('black', 'pink')],
            'solution': ['blue', 'red', 'green', 'black', 'pink'],
            'description': "3 bands per node with duplicates in 'bands'."
        },
        {
            'bands': random.sample((x := ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]), len(x)),
            'intersections': random.sample((x := [("A","B","C"), ("B","C","D"), ("C", "D"), ("D","E"), ("E","F"), ("F","G"), ("G","H"), ("H","I"), ("I","J")]), len(x)),
            'solution': ["A", "B", "C", "D", "E", "F", "G", "H", "I" ,"J"],
            'description': "10 bands total."
        },
        {
            'bands': ['red', 'green', 'blue', 'pink'],
            'intersections': [('red', 'green', 'pink'), ('green', 'blue', 'pink'), ('blue', 'red', 'pink')],
            'solution': ['Cycle for red -> green -> blue -> red'],
            'description': 'Network contains cycle (reactivation).'
        },
        {
            'bands': ['red', 'green', 'blue', 'pink', 'black', 'orange'],
            'intersections': [('red', 'green', 'pink'), ('green', 'blue', 'pink'), ('blue', 'red', 'pink'), ('black', 'red', 'green'), ('orange', 'black')],
            'solution': ['Cycle for red -> green -> blue -> red'],
            'description': 'Network contains cycle (reactivation) with bands surrounding cycle.'
        },
        {
            'bands': ['G56', 'L49', 'L96', 'L109', 'L112', 'G56', 'L59', 'G83'], 
            'intersections': [('L109', 'L96', 'L49', 'G56'), ('L112', 'G56'), ('G56', 'L59'), ('G56', 'G83')],
            'solution': ['Designed to fail.'], 
            'description': 'Europa test region network (incomplete data).'
        }
    ]
    return tests

def run_data():
    print("Determines relative ages for Europa bands.")
    data = get_data()
    
    for idx, element in enumerate(data):
        # Create a BandNetwork object
        network = BandNetwork(
            bands=element['bands'],
            intersections=element['intersections'],
            confidences=element['confidences']
        )

        if network.check_cycle():
            if network.break_cycle():
                print(f"""NETWORK #{idx + 1}: {colored("CYCLE (FIXED)", "yellow")}
                Bands: \t\t{network.get_bands()}
                Intersections: \t{network.get_intersections()}
                Description: \t{element['description']}
                Cycles: \t{network.find_cycle()}
                Sorted: \t{network.sorted}
                Deviation: \t{network.calculate_accuracy()}
                """)
            else:
                print(f"""NETWORK #{idx + 1}: {colored("CYCLE (COULD NOT FIX)", "red")}
                Bands: \t\t{network.get_bands()}
                Intersections: \t{network.get_intersections()}
                Description: \t{element['description']}
                Cycles: \t{network.find_cycle()}
                """)
        else:
            label = colored("FREE OF CYCLES", "green")
            print(f"""NETWORK #{idx + 1}: {label}
                Bands: \t\t{network.get_bands()}
                Intersections: \t{network.get_intersections()}
                Description: \t{element['description']}
                Sorted: \t{network.sorted}
                Deviation: \t{network.calculate_accuracy()}
                """)

def get_data():
    # Example data - replace with your own
    data = [
        {
            'bands': ['red', 'green', 'blue', 'black'],
            'intersections': [('blue', 'red'), ('blue', 'green'), ('red', 'green'), ('green', 'black')],
            'confidences': [5, 5, 5, 5],
            'description': "2 bands per node."
        },
        {
            'bands': ['red', 'green', 'blue', 'black'], 
            'intersections': [('blue', 'red', 'pink'), ('blue', 'green', 'orange'), ('red', 'green'), ('green', 'black'), ('black', 'pink')],
            'confidences': [5, 5, 5, 5, 5],
            'description': "2 bands per node, but some nodes have extra unlisted band (which should be ignored)."
        },
        {
            'bands': ['red', 'green', 'blue', 'pink', 'black', 'orange'],
            'intersections': [('red', 'green', 'pink'), ('green', 'blue', 'pink'), ('blue', 'red', 'pink'), ('black', 'red', 'green'), ('orange', 'black')],
            'confidences': [5, 5, 3, 4, 5],
            'description': 'Network contains cycle (reactivation) with bands surrounding cycle.'
        },
        {
            'bands': ['red', 'green', 'blue'],
            'intersections': [('red', 'green'), ('green', 'blue'), ('blue', 'red')],
            'confidences': [5, 5, 5],
            'description': 'Pure cycle; no other bands.'
        }
    ]
    return data

print("Welcome! To get started, either open runner.py and input your data in get_data(), or try out some tests.")
ans = int(input("Run tests (1) or run on input data (2)? "))
match ans:
    case 1:
        run_tests()
    case 2:
        run_data()

