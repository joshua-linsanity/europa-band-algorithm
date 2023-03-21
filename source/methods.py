# Methods for the BandNetwork class.

from collections import defaultdict
from math import sqrt
import random

def topological_sort(bands, intersections):
    """Sorts band network by relative age."""
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

    # Perform a topological sort on the graph to get the relative ordering of the bands
    stack = []
    visited = set()
    for band in bands:
        if band not in visited:
            recurse_top_sort(graph, band, visited, stack)
    
    # Return sorted list
    return stack


def recurse_top_sort(graph, band, visited, stack):
    """Recurses down until bottom node, then appends to stack."""
    visited.add(band)
    for neighbor in graph[band]:
        if neighbor not in visited:
            recurse_top_sort(graph, neighbor, visited, stack)
    stack.append(band)


def calculate_accuracy(bands, intersections, sorted):
    deviation = 0

    for band in bands:
        # Create temp list and expected list without specific band
        temp = [x for x in bands if x != band]
        expected = [x for x in sorted if x != band]

        # Calculate sorted version of new band
        trial = topological_sort(temp, intersections)

        # Square the distance between old and new positions of each band
        for ele in expected:
            deviation += (trial.index(ele) - expected.index(ele))**2 / (len(bands) - 1)

    return sqrt(deviation)


def dfs_cycle_detection(bands, intersections):
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


# TODO: EXPERIMENTAL METHODS

# TODO: modify MCMC model to account for duplicate bands
# TODO: modify MCMC model to ignore irrelevant bands


def markov_chain_monte_carlo(bands, intersections):
    """Implements Markov chain Monte Carlo to find most probable ordering."""
    # Verify that all bands mentioned in intersections are present in bands
    unlisted_bands = []
    unlisted = False
    for intersection in intersections:
        for band in intersection:
            if band not in bands:
                # raise ValueError(f"Band '{band}' is mentioned in `intersections` but not in `bands`.")
                unlisted_bands.append(band)
                unlisted = True
    if unlisted:
        return f"ERROR: Bands {unlisted_bands} are mentioned in `intersections` but not in `bands`."

    # Define a function to calculate the number of satisfied constraints for a given ordering
    def count_satisfied_constraints(ordering):
        count = 0
        
        for intersection in intersections:
            top_band = intersection[0]
            bottom_bands = intersection[1:]
            
            top_band_index = ordering.index(top_band)
            
            for bottom_band in bottom_bands:
                bottom_band_index = ordering.index(bottom_band)
                
                # Count successes: top is above bottom
                if top_band_index < bottom_band_index:
                    count += 1
        
        return count
    
    # Define a function to propose a new ordering by swapping two bands
    def propose_new_ordering(ordering):
        i = random.randint(0, len(ordering) - 1)
        j = random.randint(0, len(ordering) - 1)
        
        new_ordering = list(ordering)
        new_ordering[i], new_ordering[j] = new_ordering[j], new_ordering[i]
        
        return tuple(new_ordering)
    
    # Initialize variables
    n_samples = 10000
    burn_in = 1000
    
    current_ordering = tuple(bands)
    current_count = count_satisfied_constraints(current_ordering)
    
    counts = {}
    
    # Run MCMC algorithm
    for i in range(n_samples + burn_in):
        proposed_ordering = propose_new_ordering(current_ordering)
        proposed_count = count_satisfied_constraints(proposed_ordering)
        
        if proposed_count >= current_count or random.random() < (proposed_count / current_count):
            current_ordering = proposed_ordering
            current_count = proposed_count
        
        if i >= burn_in:
            if current_ordering not in counts:
                counts[current_ordering] = 0
            
            counts[current_ordering] += 1
    
    # Find most probable ordering
    most_probable_ordering = max(counts.items(), key=lambda x: x[1])[0]
    
    return list(most_probable_ordering)
