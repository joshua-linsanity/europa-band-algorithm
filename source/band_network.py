# BandNetwork class implementation

import os
import itertools
from typing import List, Tuple
from collections import defaultdict
from math import sqrt

# BandNetwork class to represent a series of bands and intersections.
class BandNetwork:
    def __init__(self, bands: List[str], intersections: List[Tuple[str]], confidences: List[int] = None):
        """Instantiate current object."""
        self.bands = bands
        self.intersections = intersections
        self.confidences = confidences
        self.sorted = self.top_sort()
        self.excluded = None

    def __str__(self):
        """to_string method for current BandNetwork object."""
        to_string = "Band Network with {num_bands} bands and {num_int} intersection nodes."
        return to_string.format(num_bands = len(self.bands), num_int = len(self.intersections))

    # Getters and setters
    def get_bands(self):
        """Returns list of bands."""
        return self.bands

    def get_intersections(self):
        """Returns list of intersections."""
        return self.intersections

    def get_confidences(self):
        """Returns list of confidences."""
        return self.confidences

    def set_bands(self, bands):
        """Changes bands to specified list."""
        self.bands = bands

    def set_intersections(self, intersections):
        """Changes intersections to specified list."""
        self.intersections = intersections

    def set_confidences(self, confidences):
        self.confidences = confidences

    # Primary Methods
    def top_sort(self):
        """Perform a topological sort on the graph to get the relative ordering of the bands."""
        return top_sort_helper(self.bands, self.intersections)

    def calculate_accuracy(self):
        """Rank network ordering based on consistency after removal."""
        deviation = 0

        for band in self.sorted:
            # Create temp list and expected list without specific band
            temp = [x for x in self.bands if x != band and x in self.sorted]
            expected = [x for x in self.sorted if x != band]

            # Calculate sorted version of new band
            trial = top_sort_helper(temp, self.intersections)

            # Square the distance between old and new positions of each band
            for ele in expected:
                deviation += (trial.index(ele) - expected.index(ele))**2 / (len(self.sorted) - 1)

        return sqrt(deviation)

    def check_cycle(self):
        return check_cycle_helper(self.bands, self.intersections)

    def find_cycle(self):
        """Find reactivated (cycle) bands in band network."""
        find_cycle_helper(self.bands, self.intersections)
        cycles = []
        with (open("output.txt", "r")) as f:
            lines = f.readlines()
            for line in lines:
                if (line.count(" ") == 1):
                    continue
                cycles.append(line.split())
        os.remove("output.txt")        
        return cycles

    def break_cycle(self):
        """Remove all lower confidence intersections to try and break the cycle."""
        if self.confidences is None:
            raise ValueError("Initialize with set_confidences() first!")
        if len(self.intersections) != len(self.confidences):
            raise ValueError("intersections[] and confidences[] need to have same length.")

        # Start by removing lowest confidence level, then increment until highest
        cutoff_confidence = min(self.confidences)
        while cutoff_confidence < max(self.confidences):
            trial_bands, trial_intersections = [], []
            # Add all intersections above the current confidence cutoff
            for (i, c) in itertools.zip_longest(self.intersections, self.confidences):
                if (c > cutoff_confidence):
                    trial_intersections.append(i)
            # Add all bands within these intersections
            for ti in trial_intersections:
                for b in ti:
                    trial_bands.append(b)
            # If there is no cycle, return True
            if not check_cycle_helper(trial_bands, trial_intersections):
                self.sorted = top_sort_helper(trial_bands, trial_intersections)
                return True
            # Otherwise, eliminate next confidence level
            else:
                cutoff_confidence += 1
        # If unable to break cycle, return False
        return False

# Graph class for applying Kosaraju's Algorithm to find strongly connected components.
class Graph:
    def __init__(self, vertex):
        self.V = vertex
        self.graph = defaultdict(list)
        self.output = 'output.txt'

    # Add edge into the graph
    def add_edge(self, s, d):
        self.graph[s].append(d)

    # dfs
    def dfs(self, d, visited_vertex):
        visited_vertex[d] = True
        with open(self.output, 'a') as f:
            f.write(f"{d} ")
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.dfs(i, visited_vertex)

    def fill_order(self, d, visited_vertex, stack):
        visited_vertex[d] = True
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)
        stack = stack.append(d)

    # transpose the matrix
    def transpose(self):
        g = Graph(self.V)

        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g

    # Finds strongly connected components
    def find_scc(self):
        stack = []
        visited_vertex = defaultdict(lambda: False)

        keys = list(self.graph.keys())
        for i in keys:
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)

        gr = self.transpose()

        visited_vertex = defaultdict(lambda: False)

        while stack:
            i = stack.pop()
            if not visited_vertex[i]:
                gr.dfs(i, visited_vertex)
                with open(self.output, 'a') as f:
                    f.write('\n')

def create_adj_list(bands, intersections):
    """Helper Function: creates directed graph with below bands pointing to top bands."""
    # Create a dictionary to store the adjacency list representation of the graph
    graph = defaultdict(list)

    # Iterate over the intersection tuples and add directed edges to the graph
    for intersection in intersections:
        # Ignore any bands that aren't in `bands`
        if (top_band := intersection[0]) not in bands:
            continue
        for below_band in intersection[1:]:
            # Ignore any bands that aren't in `bands`
            if below_band not in bands:
                continue
            graph[below_band].append(top_band)
    return graph

def top_sort_helper(bands, intersections):
    def recurse(graph, band, visited, stack):
        """Helper Function: recurses down until bottom node, then appends to stack."""
        visited.add(band)
        for neighbor in graph[band]:
            if neighbor not in visited:
                recurse(graph, neighbor, visited, stack)
        stack.append(band)

    graph = create_adj_list(bands, intersections)
    stack = []
    visited = set()
    for band in bands:
        if band not in visited:
            recurse(graph, band, visited, stack)
    
    # Return sorted list
    return stack

def check_cycle_helper(bands, intersections):
    """Detects cycle (reactivation) in graph."""
    
    # Visits all neighboring nodes.
    def dfs_visit(graph, band, visited, rec_stack):
        """Visits neighbor nodes."""
        visited.add(band)
        rec_stack.add(band)
        for neighbor in graph[band]:
            if neighbor not in visited:
                if dfs_visit(graph, neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.remove(band)
        return False

    # Create a dictionary to store the adjacency list representation of the graph
    graph = defaultdict(list)

    # Iterate over the intersection tuples and add directed edges to the graph
    for intersection in intersections:
        top_band = intersection[0]
        for below_band in intersection[1:]:
            graph[below_band].append(top_band)

    # Perform a depth-first search on each node to detect cycles
    visited = set()
    rec_stack = set()
    for band in bands:
        if dfs_visit(graph, band, visited, rec_stack):
            return True
    return False

def find_cycle_helper(bands, intersections):
    g = Graph(len(bands))
    for key, values in create_adj_list(bands, intersections).items():
        for v in values:
            g.add_edge(key, v)
    g.find_scc()
