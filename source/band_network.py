# BandNetwork class implementation

from methods import *
from typing import List

class Band:
    """Represents one band with its name and feature type."""
    index = 0
    def __init__(self, name=f"Band #{index + 1}", type=None) -> None:
        self.name = name
        self.type = type
        index += 1
        

class Node:
    """Represents one intersection with bands and confidence."""
    def __init__(self, top: str, bottom: List(str), confidence: int) -> None:
        self.top = top
        self.bottom = bottom
        self.confidence = confidence if 1 <= confidence <= 5 else None

class Test:
    """Represents one test case."""

    def __init__(self, bands: List(Band), intersections: List(Node), solution: List(str), description: str):
        self.bands = bands
        self.intersections = intersections
        self.solution = solution
        self.description = description


class BandNetwork:
    """Represents a network of bands."""

    def __init__(self, bands, intersections):
        self.bands = bands
        self.intersections = intersections
        self.sorted = self.probabilistic_sort()

    def unique_sort(self):
        """Sorts band network with unique solution."""
        return topological_sort(self.bands, self.intersections)
    
    def probabilistic_sort(self):
        # TODO: modify algorithm
        """Sorts band network using Markov Chain Monte Carlo."""
        return markov_chain_monte_carlo(self.bands, self.intersections)

    def detect_cycle(self):
        return dfs_cycle_detection(self.bands, self.intersections)

    def get_deviation(self):
        """Rank network ordering based on consistency after removal."""
        return calculate_accuracy(self.bands, self.intersections, self.sorted)
