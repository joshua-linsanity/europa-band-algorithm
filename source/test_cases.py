import random
from band_network import *

tests = {}
tests[1] = Test(
    bands = make_bands(['red', 'green', 'blue', 'black']),
    intersections = make_intersections([('blue', 'red'), ('blue', 'green'), ('red', 'green'), ('green', 'black')]),
    solution = ['blue', 'red', 'green', 'black'],
    description = "2 bands per node."
)
tests[2] = Test(
    bands = make_bands(['red', 'green', 'blue', 'black']),
    intersections = make_bands([('blue', 'red', 'pink'), ('blue', 'green', 'orange'), ('red', 'green'), ('green', 'black'), ('black', 'pink')]),
    solution = ['blue', 'red', 'green', 'black'],
    description = "2 bands per node, with extra unlisted bands (ignored)."
)
tests[3] = Test(
    bands = make_bands(['red', 'blue', 'black', 'green', 'pink']),
    intersections = make_intersections([('blue', 'pink', 'red'), ('blue', 'green', 'pink'), ('red', 'green', 'pink'), ('green', 'black'), ('black', 'pink')]),
    solution = ['blue', 'red', 'green', 'black', 'pink'],
    description = "3 bands per node."
)
tests[4] = Test(
    bands = make_bands(random.sample((x := ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]), len(x))),
    intersections = make_intersections(random.sample((x := [("A","B","C"), ("B","C","D"), ("C", "D"), ("D","E"), ("E","F"), ("F","G"), ("G","H"), ("H","I"), ("I","J")]), len(x))),
    solution = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    description = "10 bands total."
)
tests[5] = Test(
    bands = make_bands(['red', 'green', 'blue', 'pink']),
    intersections = make_intersections([('red', 'green', 'pink'), ('green', 'blue', 'pink'), ('blue', 'red', 'pink')]),
    solution = ['Cycle for red -> green -> blue -> red'],
    description = "Network contains cycle (reactivation)."
)
# {
    # # TODO: update bands + remove duplicates
    # 'bands': ['G56', 'L49', 'L96', 'L109', 'L112', 'G56', 'L59', 'G83'], 
    # # TODO: finish intersections
    # 'intersections': [('L109', 'L96', 'L49', 'G56'), ('L112', 'G56'), ('G56', 'L59'), ('G56', 'G83')],
    # # TODO: determine solution
    # 'solution': ['Not implemented yet'], 
    # 'description': 'Europa test region network (incomplete data).'
# }

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
