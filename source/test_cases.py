import random
from band_network import *

def get_tests() -> List(Test):
    # Duplicates in 'bands' list will automatically be removed.

    tests = []
    tests.append(
        Test(
            [Band('red'), Band('green'), Band('blue'), Band('black')],
            [Node('blue', ['red']), Node('blue', ['green']), Node('red', ['green']), Node('green', ['black'])],
            ['blue', 'red', 'green', 'black'],
            "2 bands per node."
        )
    )

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
        # {
        #     'bands': ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J","K","L","M","N","O","P","Q","R","S","T"],
        #     'intersections': [("A","B","C","D"), ("B","C"), ("C","D"), ("D","E"), ("E","F"), ("F","G"), ("G", "H"), ("H", "I"),("I", "J"), ("J", "K"), ("K", "L"), ("L", "M"), ("M", "N"), ("N", "O"), ("O", "P"), ('P', 'Q'), ('Q', 'R'), ('R', 'S'), ('S', 'T')],
        #     'solution': ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
        #     'description': "20 bands total."
        # },
        # {
        #     'bands': random.sample([str(i) for i in range(1, 101)], 100),
        #     'intersections': [(str(i), str(i+1), str(i+2), str(i+3)) for i in range(1,98)] + [(98, 99, 100), (99, 100)],
        #     'solution': [str(i) for i in range(1, 101)],
        #     'description': "100 bands total."
        # },
        {
            'bands': ['red', 'green', 'blue', 'pink'],
            'intersections': [('red', 'green', 'pink'), ('green', 'blue', 'pink'), ('blue', 'red', 'pink')],
            'solution': ['Cycle for red -> green -> blue -> red'],
            'description': 'Network contains cycle (reactivation).'
        },
        {
            # TODO: update bands + remove duplicates
            'bands': ['G56', 'L49', 'L96', 'L109', 'L112', 'G56', 'L59', 'G83'], 
            # TODO: finish intersections
            'intersections': [('L109', 'L96', 'L49', 'G56'), ('L112', 'G56'), ('G56', 'L59'), ('G56', 'G83')],
            # TODO: determine solution
            'solution': ['Not implemented yet'], 
            'description': 'Europa test region network (incomplete data).'
        }
    ]
    my_dict = {}
    dict2 = {}
    for element in random.sample((x := [("A","B","C"), ("B","C","D"), ("C", "D"), ("D","E"), ("E","F"), ("F","G"), ("G","H"), ("H","I"), ("I","J")]), len(x)):
        my_dict[element] = 'high'
    for element in [("A","B","C"), ("D","E","F"), ("G","H","I"), ("J","A"), ("B","D"), ("C","G")]:
        dict2[element] = 'high'

    test_dicts = [
        {
            'bands': ['red', 'blue', 'black', 'green', 'pink'],
            'intersections': {('blue', 'pink', 'red'): 'high', ('blue', 'green', 'pink'): 'high', ('red', 'green', 'pink'): 'high', ('green', 'black'): 'high', ('black', 'pink'): 'high'},
            'solution': ['blue', 'red', 'green', 'black', 'pink'],
            'description': "3 bands per node."
        },
        {
            'bands': random.sample((x := ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]), len(x)),
            'intersections': my_dict,
            'solution': ["A", "B", "C", "D", "E", "F", "G", "H", "I" ,"J"],
            'description': "10 bands total."
        },
        {
            'bands': ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            'intersections': dict2,
            'solution': ["J", "A", "B", "D", "E", "F", "C", "G", "H" ,"I"],
            'description': 'Bing-generated Network'
        }
    ]

    return tests, test_dicts

def add_test(tests):
    bands, intersections, solution = [], [], []
    print("""
        Bands: enter each name, ex: 'red'
        Intersections: enter each node, ex: 'red, green, blue'
        Solution: enter each band young to old, ex: 'blue'
        Press 'stop' to reach next input at any point.
        """)

    # Get bands
    while True:
        new = input("Band: ")
        if new.lower() == 'stop':
            break
        bands.append(new)
    
    # Get intersections
    while True:
        new = input("Intersection: ")
        if new.lower() == 'stop':
            break
        intersections.append(new.split(", "))
    
    # Get solution
    while True:
        new = input("Next band: ")
        if new.lower() == 'stop':
            break
        solution.append(new)

    return

def remove_test(tests):
    tests.pop()

def remove_test(tests, idx):
    tests.pop(idx)
