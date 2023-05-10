# europa-band-algorithm
Project to sort bands on Europa's ice-shell lithosphere by relative age. Findings from both geological analysis (separate) and relative ages algorithm (this project) presented at the [NASA Jet Propulsion Lab (JPL)](https://www.jpl.nasa.gov/) in Pasadena on May 12th, 2023. 
* Research Coordinators: [Dr. Robert Pappalardo](https://science.jpl.nasa.gov/people/pappalardo/) (Europa Clipper Project Scientist), [Dr. Erin Leonard](https://science.jpl.nasa.gov/people/leonard/) (Europa Clipper Staff Scientist), [Dr. Michelle Selvans](https://airandspace.si.edu/people/staff/michelle-selvans) (Clovis Community College).
* Team Members: Joshua Lin, Cheyanne Macagno, Malika Neal, David Baize II, Scott Phillips.

*This Python project was written by Joshua Lin.*

Image mosaics analyzed from [NASA Galileo's Solid-State Imager](https://astrogeology.usgs.gov/search/map/Europa/Mosaic/Equirectangular_Mosaics_of_Europa_v3):

![alt text](https://astrogeology.usgs.gov/cache/images/1ca8fca37b10e3db141f165ce9990965_Europa_mosaic_thumbnail_xl.JPG "Galileo Mosaics")

# Abstract

Analyzing the intersections of Europan bands can divulge information about their relative ages. By considering the youngest bands at each intersection while noting the subsequent unordered older bands contained underneath, we administer an algorithm rooted in topological sorting to determine a unique ordering of the bands when possible. In addition, displaying the deviation from a unique solution is useful for considering which networks may have a more or less accurate ordering. To calculate the error for non-unique solutions, we sum the squares of the elements’ displacements upon removal of any given band. Ultimately, we implement a detection algorithm that locates potential spots of geological reactivation, identifying the specific bands whose intersections form strongly connected components, and break the cycle automatically if possible by eliminating low-confidence intersections.

# Background
* **Depth First Search (DFS)** is an algorithm to traverse the nodes within a graph. The algorithm selects an arbitrary root node within a graph and then explores as far as possible (“depth first”) along every branch of that graph before backtracking. When every branch of a node has been explored 
* **Topological sort** is an algorithm that orders the nodes in a Directed Acyclic Graph (DAG) such that for every directed edge u→v, u arrives prior to v in the ordering. Applying top sort to the network of intersections on Europa therefore offers a way to categorize the relative ages of every band within the network. “Top” sort works in this case by implementing DFS, as explained above.
* **Underdetermined systems** describes the fact that there may not exist enough intersections to determine a unique ordering of the bands. In essence, an n-band system would require at worst n-1 intersections (if each intersection contained 2 bands) to find a unique ordering. But even when more bands are present at an intersection, the widespread nature of bands often means that there is not sufficient data to uniquely sort the network (although any solution will conform to the intersection data present, as per topological sort).
* **Reactivation** is a geologic process by which bands on Europa’s surface halt signification expansion for a period of time, before then proceeding to restart. As a result, when reactivation is present, any algorithm may determine that for bands A, B, and C, the relative ages (from oldest to youngest) flow as A→B→C→A. In other words, for band networks in which reactivation occurs, there will always be a cycle—which has length 3 in the example above—which therefore breaks topological sort (recall that one condition is that the graph be acyclic).
* **Cycle Detection** is a method by which cycles in a graph are found. In this case, DFS is used to determine whether or not cycles exist within the band network. Broadly, suppose that during DFS, the currently visited node is arrived at again—then, there clearly is a cycle from one band to itself.
* **Kosaraju’s Algorithm** is a method of separating a graph into each of its respective cycles, or strongly connected components (SCC). A strongly connected component is a section of a graph in which each element can arrive (along the directed edges) at any other element. Kosaraju’s algorithm broadly works by first applying DFS to the entire graph, keeping track of a “stack” of nodes who have all their child nodes visited already when arrived at. Then, reverse the directed edges of the graph and apply DFS again on the reversed graph. Starting at the end of the original stack, traverse along the directed edges; when we arrive at a node with all its children visited, that is the end of the strongly connected component. Kosaraju’s Algorithm will find all of SCCs. 

# Methodology
To represent a network of intersecting bands on Europa, we created the BandNetwork class, which has two instance variables: 
* *bands*: a list of the names of all bands to be sorted.
* *intersections*: a list of string tuples. Each tuple is formatted such that the first string denotes the youngest band at the intersection (the one on top), while subsequent strings are the older bands in no particular order.
* *confidences*: a list of integers, representing the confidence levels of each corresponding index’s intersection on a scale from low to high (e.g., 1 to 3, 1 to 5, etc.)
Every BandNetwork object has four getters/setters for bands and intersections, but also several useful instance methods for analysis of the network:
* *top\_sort()*: Ranks the bands in order of relative age (youngest to oldest) using topological sort. Returns List[str].
* *calculate\_accuracy()*: Quantifies the accuracy of a particular sorting. For every band in bands, remove it from the original sorting. Then, re-run sort() without that band. Compare the results by adding up the root-mean-square of the index differences of every band’s position in the two lists. Returns float.
* *check\_cycle()*: Applies DFS cycle detection to determine whether or not reactivation exists within the network. Returns bool. 
* *find\_cycle()*: Applies Kosaraju’s Algorithm to find all reactivation cycles within the band network (i.e., strongly connected components of length > 1). Returns List[List[str]].
* *break\_cycle()*: If a cycle is detected, automatically try to break it. Do this by removing the lowest confidence level bands, one level at a time, until the resultant topological sort ordering contains no cycle. If the cycle cannot be broken before removing all confidence levels, print the bands causing the original cycle.

Because topological sort is most accurate for unique orderings, we calculate the accuracy of each sorting. If there is a high deviation, then the sorting is unlikely to be accurate—likely due to the network being underdetermined. Note that a perfectly accurate ordering would have a deviation of 0.

Reactivation will be automatically detected upon outputting the data. If *check\_cycle()* returns true, then there must be geological reactivation at some point within the data. The bands within all cycles (even if there are multiple cycles) are then found and outputted. If the cycle can be broken by removing lower-confidence intersections, it will be.

Usage: to run on specific networks, add the bands, intersections, confidences, and description parameters to the *get\_data()* function in runner.py, which has some examples with proper formatting.

# Discussion/Results

Because the network is generally underdetermined, considering the fact that there are significantly fewer intersections than required to determine a unique sorting, it is very unlikely that a sorted solution will be completely accurate. 

Therefore, this Python program is most useful for 1) obtaining a general idea of the relative ages of bands, using the deviation calculation to determine how the accuracy of topological sort, and 2) finding cycles within the network to identify geological reactivation—which may then be resolved manually, if need be. 

