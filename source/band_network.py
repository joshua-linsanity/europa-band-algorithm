# BandNetwork class implementation

from methods import *
from typing import List, Tuple, Optional

class Band:
    """Represents one band with its name and feature type."""
    def __init__(self, name="Unnamed Band", type=None) -> None:
        self.name = name
        self.type = type
    
class Intersection:
    """Represents one intersection with bands and confidence."""
    def __init__(self, top: str, bottom: List[str], confidence: Optional[int]=None) -> None:
        self.top = top
        self.bottom = bottom
        self.confidence = confidence

class Test:
    """Represents one test case."""
    def __init__(self, bands: List[Band], intersections: List[Intersection], solution: List[str], description: str):
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


# TODO: NON-CLASS METHODS
def make_bands(bands: List[str], types: Optional[List[str]]=None) -> List[Band]:
    band_list = []
    if types is None:
        for band in bands:
            band_list.append(Band(name=band))
    else:
        if len(bands) != len(types):
            raise ValueError("bands and types are not of same length.")
        for band, type in zip(bands, types):
            band_list.append(Band(name=band, type=type))
    return band_list

def make_intersections(intersections: List[Tuple[str, ...]], confidences: Optional[List[int]]=None) -> List[Intersection]:
    intersection_list = []
    if confidences is None:
        for intersection in intersections:
            intersection_list.append(Intersection(top=intersection[0], bottom=intersection[1:]))
    else:
        for intersection, confidence in zip(intersections, confidences):
            intersection_list.append(Intersection(top=intersection[0], bottom=intersection[1:], confidence=confidence))
    return intersection_list
