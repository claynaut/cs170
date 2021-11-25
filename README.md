# CS170 (Intro to AI) Project Files
Source code for CS170 projects (Intro to AI). Original specifications are authored by the instructor for the course, and other sources used are referenced in the respective project directories.

## File Structure
Each project has their own directory denoted by `project-[number]` and contains the original source code. Each project is described in the root `README` file.

## Project 1: Eight Puzzle
### Objective
Solve the eight puzzle, a 3 x 3 sliding tile puzzle with 8 tiles, using three search algorithms and analyze the results.

Three search algorithms in question:
- Uniform Cost Search
- A* with Misplaced Tile Heuristic
- A* with Manhattan Distance Heuristic

### Overview
The main code used to solve the eight puzzle is `nPuzzle.py` which has also been modified to try to solve any custom puzzle where the user determines the start state and goal state.

### Sources Consulted
- Heuristic Search, Blind Search, and Eight Puzzle Briefing lecture slides provided by Dr. Keogh
- Project 1 specificatons provided by Dr. Keogh
- [Python 3.10.0 documentation](https://docs.python.org/)
- [Any Python Three documentation](https://anytree.readthedocs.io/)

## Project 2: Feature Selection with Nearest Neighbor
### Objective
Perform feature selection with the nearest neighbor classifier using two kinds of searches:

Two search algorithms in question:
- Forward Selection
- Backward Elimination

### Overview
The main code used to perform feature selection is `featureSelection.py` which prompts for a dataset to test. Note that this works only with .txt files as it was coded to specifically parse the datasets given by the instructor.

### Sources Consulted
- Project 2 specificatons provided by Dr. Keogh
- [K Nearest Neighbor Article](https://towardsdatascience.com/k-nearest-neighbours-introduction-to-machine-learning-algorithms-18e7ce3d802a)
    - Referred to for pseudocode and further understanding of the KNN algorithm
- [Python 3.10.0 documentation](https://docs.python.org/)
- [Any Python Three documentation](https://anytree.readthedocs.io/)