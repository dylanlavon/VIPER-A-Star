# VIPER PATHFINDING USING HPC

The goal of this project is to develop an understanding of pathfinding algorithms and how they could be used, particularly in an HPC environment, to calculate optimal paths for lunar rovers such as *VIPER*.
<br><br>
## To Do:
- [x] Add a timer
- [x] Support diagonal movement
- [x] Add octile heuristic
- [ ] Add edge weights
- [x] Heightmap-to-pathfinding-map-data converter
- [x] Load pathfinding map data from a file
- [ ] No-visualization mode / Only show final path
<br><br>
## Using astar.py
**Runs the A\* Pathfinding visualization.**

In a new grid, the first left click will place the start node (teal). The second left click will place the goal node (orange). Any left clicks after these two nodes are placed will be barrier nodes (black).

Nodes can be erased by using right click.

A grid can be cleared by pressing the "C" key.

Hitting the spacebar will start the algorithm, as long as the start and goal nodes are placed on the grid.

After the algorithm completes, the elapsed time will display in the console output.

---

Arguments: 
- _heuristic_, **required**, positional: Tell the script which heuristic function to use. [manhattan, euclidean, octile]
- _size_: Width/height of the grid; 50 by default. Will be overwritten by the size of a map if using --use_map.
- _use_map_: The full name of an image in the _maps_ subdirectory. Defines barrier/empty nodes. Replaces the size of the grid if using _size_. 

<br><br>
## Using img_to_grid.py
**Convert a square image into a map for use in astar.py.**

Downscales an image to the specified size, and optionally clamps pixels to black or white using the value provided for the _binary_ flag.

For example, if a value supplied for _binary_ is **.5**, any pixel that has a brightness of 128 (50% of the max value, 255, aka white) or higher will be set to white. Otherwise, it will be **black**.

Pixels are required to be **black** to register as barriers in _astar.py_.

Arguments: 
- _source_img_, **required**, positional: Tell the script which image to use in the _source_images_ subdirectory.
- _size_, **required**, positional: Width/height of the of the new map image. Must be smaller than the original image.
- _binary_: Threshold used to set pixels to either black (barrier) or white (empty node). A higher value means more barriers. Float value between 0 and 1.

<br><br>
## Resources

[A* Literature](https://www.sciencedirect.com/science/article/pii/S1877050921000399?via%3Dihub)

[Algorithm Visualization Base](https://www.youtube.com/watch?v=JtiK0DOeI4A&ab_channel=TechWithTim)

---
For CENG6332 - High Performance Computer Architecture.

Dylan Britain

Dr. Liwen Shih, University of Houston - Clear Lake, Spring 2025

---
