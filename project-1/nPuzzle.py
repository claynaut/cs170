from anytree import Node # nodes used to create a tree
import copy # deep copy used to make a copy of a value to avoid alterating a reference
import time # used to record how long it took to run the search

# collection of start states given by project specs from the instructor
depth_0 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
depth_2 = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
depth_4 = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
depth_8 = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
depth_12 = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
depth_16 = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
defaults = [depth_0, depth_2, depth_4, depth_8, depth_12, depth_16]

# default goal state for a 3x3 puzzle that gets altered if a custom start state is created
goal_state = [[1, 2, 3], [4, 5 , 6], [7, 8, 0]]

# prints puzzle in console
def printPuzzle(puzzle):
    for row in puzzle: 
        print(row)

# creates an 8-puzzle based on the user's option and returns the generated 8-puzzle
def selectPuzzle():
    print('Select a puzzle to solve for this n-puzzle solver.')
    print('\t1. Use default puzzle layout')
    print('\t2. Create a custom puzzle layout')

    # retrieves user's selection for which puzzle to make
    option  = int(input('\nChoose an option: '))

    # if user selects an invalid option, loop until a valid input is made
    while option != 1 and option != 2:
        print('Error: Invalid option. Try again.')
        option  = int(input('Choose an option: '))

    # returns default puzzle layout
    if option == 1:
        print('\nUsing default puzzle layouts...')
        print('\n\t1. Depth 0')
        print('\t2. Depth 2')
        print('\t3. Depth 4')
        print('\t4. Depth 8')
        print('\t5. Depth 12')
        print('\t6. Depth 16')

        # asks user which default puzzle layout to use
        n = int(input('\nSelect a puzzle to use: '))

        # returns default puzzle
        return defaults[n-1]

    # creates a custom puzzle layout
    elif option == 2:
        print('\nCreating custom puzzle layout...')
    
        # asks user for the size of the puzzle
        n = int(input('\nEnter length n of puzzle (i.e. size of puzzle = n x n): '))

        # array used to validate user input (numbers determined by the size of the puzzle)
        possible_numbers = list(range(n*n))

        # array used to validate user input (checked to make sure user doesn't input duplicate numbers)
        # each element is set to -1 to indicate the number is already taken
        available_numbers = list(range(n*n))

        # clear goal state to create a new goal state based on the custom puzzle layout
        goal_state = []
        for i in range(n):
            # appends an array from a range starting at 1 (which is why a 1 is added)
            # and uses i and n to calculate the start and of the ranges
            goal_state.append(list(range(i*n+1, (i+1)*n+1)))
        goal_state[n-1][n-1] = 0 # sets the bottom right corner to a 0 to indicate a blank space

        # generate empty puzzle to fill in by user input
        puzzle = []
        for i in range(n):
            puzzle.append([])

        # creates first row of the puzzle

        for i in range(len(puzzle)):
            print('Enter row ' + str(i+1) + ':')
            # for loop ran n times for n numbers in a row
            for j in range(n):
                # retrieves user's input for a number in the row
                element = int(input())

                # check if the number selected is in the possible numbers to select from
                # otherwise, loop until the user inputs a valid number
                while (not (element in possible_numbers)):
                    print('Error: Invalid input. Select numbers from 0-' + str(len(possible_numbers)-1) + '.')
                    element = int(input())

                # check if the number selected hasn't already been taken (to avoid duplicate numbers)
                # otherwise, loop until the user inputs a valid number
                while (not (element in available_numbers)):
                    print('Error: Duplicate value. Number already added to puzzle.')
                    element = int(input())

                # set chosen number in the array of available numbers to -1
                # to indicate the number has been taken
                available_numbers[available_numbers.index(element)] = -1

                # add number to the row
                puzzle[i].append(element)

        # returns user-created puzzle
        return puzzle

# asks user which algorithm to use and returns a number indicating which algorithm to use
def selectAlgorithm():
    print('\nSelect algorithm.')
    print('\t1. Uniform Cost Search')
    print('\t2. A* with Misplaced Tile heuristic')
    print('\t3. A* Manhattan Distance heuristic')

    # retrieves user's selection on which algorithm to use
    option  = int(input('\nChoose an option: '))

    # if user selects an invalid option, loop until a valid input is made
    while option != 1 and option != 2 and option != 3:
        print('Error: Invalid option. Try again.')
        option  = int(input('Choose an option: '))

    # returns user's selection
    return option

# prints out which algorithm will be used and calls the respective function for that algorithm
def runAlgorithm(option, problem):
    # runs algorithm for uniform cost search
    if option == 1:
        print('\nSolving with Uniform Cost Search...')
        return search(problem, 0)

    # runs algorithm for A* with misplaced tile heuristic
    elif option == 2:
        print('\nSolving with A* with Misplaced Tile heuristic...')
        return search(problem, 1)

    # runs algorithm for A* with manhattan distance heuristic
    elif option == 3:
        print('\nSolving with A* Manhattan Distance heuristic...')
        return search(problem, 2)

# gets location of provided tile within provided puzzle
def getTileLocation(puzzle, number):
    # checks each row if the number exist
    for row in range(len(puzzle)):
        # if number exists in the row, returns location [row, column]
        if number in puzzle[row]:
            return [row, puzzle[row].index(number)]

# calculates h(n) based on heuristic chosen
def calculateHeuristic(puzzle, heuristic):
    # if it's uniform cost search, h(n) remains 0
    h = 0

    # if it's misplaced tile heuristic
    if heuristic == 1:
        # checks each location by row and column
        for row in range(len(puzzle)):
            for col in range(len(puzzle)):
                # compares provided puzzle against goal state and increments h(n)
                # and checks that the blank state isn't counted
                if puzzle[row][col] != goal_state[row][col] and puzzle[row][col] != 0:
                    h += 1

    # if it's manhattan distance heuristic
    elif heuristic == 2:
        misplaced = [] # stores misplaced tiles
        for row in range(len(puzzle)):
            for col in range(len(puzzle)):
                # compare provided puzzle against goal state and adds to an array of misplaced tiles
                # and checks that the blank state isn't counted
                if puzzle[row][col] != goal_state[row][col] and puzzle[row][col] != 0:
                    misplaced.append(puzzle[row][col])
        # for each misplaced tile, calculates the distance from the goal state
        for tile in misplaced:
            [goal_row, goal_col] = getTileLocation(goal_state, tile) # gets location of tile in the goal state
            [curr_row, curr_col] = getTileLocation(puzzle, tile) # gets location of tile in the current state
            h += abs(goal_row - curr_row) + abs(goal_col - curr_col) # gets the difference between the two locations

    # returns calculated h(n)
    return h

# calculates f(n) based on the node's g(n) and h(n)
def calculateCost(node):
    # computes f(n) by adding g(n) which is the depth and h(n) which is the heuristic
    # and sets it as the cost attribute for the node
    node.f = node.depth + node.h

# operation to move blank space to the left
def moveLeft(puzzle):
    [blank_row, blank_col] = getTileLocation(puzzle, 0) # gets location of blank space

    # checks if it's valid to perform a move left operation so that it doesn't go out of bounds
    if blank_col == 0:
        return -1

    # creates a deep copy so original puzzle passed in isn't altered directly
    newPuzzle = copy.deepcopy(puzzle)

    # swaps locations of necessary tiles to perform respective operation
    newPuzzle[blank_row][blank_col] = newPuzzle[blank_row][blank_col-1]
    newPuzzle[blank_row][blank_col-1] = 0

    # returns the altered puzzle copy
    return newPuzzle

# operation to move blank space to the right
def moveRight(puzzle):
    [blank_row, blank_col] = getTileLocation(puzzle, 0) # gets location of blank space

    # checks if it's valid to perform a move right operation so that it doesn't go out of bounds
    if blank_col == 2:
        return -1

    # creates a deep copy so original puzzle passed in isn't altered directly
    newPuzzle = copy.deepcopy(puzzle)

    # swaps locations of necessary tiles to perform respective operation
    newPuzzle[blank_row][blank_col] = newPuzzle[blank_row][blank_col+1]
    newPuzzle[blank_row][blank_col+1] = 0

    # returns the altered puzzle copy
    return newPuzzle

# operation to move blank space up
def moveUp(puzzle):
    [blank_row, blank_col] = getTileLocation(puzzle, 0) # gets location of blank space

    # checks if it's valid to perform a move up operation so that it doesn't go out of bounds
    if blank_row == 0:
        return -1

    # creates a deep copy so original puzzle passed in isn't altered directly
    newPuzzle = copy.deepcopy(puzzle)

    # swaps locations of necessary tiles to perform respective operation
    newPuzzle[blank_row][blank_col] = newPuzzle[blank_row-1][blank_col]
    newPuzzle[blank_row-1][blank_col] = 0

    # returns the altered puzzle copy
    return newPuzzle

# operation to move blank space to down
def moveDown(puzzle):
    [blank_row, blank_col] = getTileLocation(puzzle, 0) # gets location of blank space

    # checks if it's valid to perform a move down operation so that it doesn't go out of bounds
    if blank_row == 2:
        return -1

    # creates a deep copy so original puzzle passed in isn't altered directly
    newPuzzle = copy.deepcopy(puzzle)

    # swaps locations of necessary tiles to perform respective operation
    newPuzzle[blank_row][blank_col] = newPuzzle[blank_row+1][blank_col]
    newPuzzle[blank_row+1][blank_col] = 0

    # returns the altered puzzle copy
    return newPuzzle

# expands given node and returns the children
def expandNode(node):
    children = [] # stores children of given node

    # copies puzzle in node and performs a move left operation
    move_left = copy.deepcopy(node.name)
    move_left = moveLeft(move_left)

    # copies puzzle in node and performs a move right operation
    move_right = copy.deepcopy(node.name)
    move_right = moveRight(move_right)

    # copies puzzle in node and performs a move up operation
    move_up = copy.deepcopy(node.name)
    move_up = moveUp(move_up)

    # copies puzzle in node and performs a move down operation
    move_down = copy.deepcopy(node.name)
    move_down = moveDown(move_down)

    # checks return value of each operation
    # and if operation was valid, the result is added to array of children
    if move_left != -1:
        children.append(move_left)
    if move_right != -1:
        children.append(move_right)
    if move_up != -1:
        children.append(move_up)
    if move_down != -1:
        children.append(move_down)

    # returns an array of children to assign to the provided node
    return children

# general search function
def search(problem, heuristic):
    root = Node(problem[0]) # sets start state as the root node
    goal = Node(problem[1]) # defines goal state as a node
    nodes = [root] # places root into queue
    nodesExpanded = 0 # keeps track of nodes expanded
    maxQueueSize = 1 # keeps track of max queue size

    while 1:
        # if queue is empty, print failure
        if not nodes:
            print('Failure!')
            return

        # sets current node to the node at the front of the queue
        current_node = nodes.pop(0)

        # if goal state is reached, print statistics
        if current_node.name == goal.name:
            print('Goal state reached!')
            print('\nSolution depth:', current_node.depth)
            print('Nodes expanded:', nodesExpanded)
            print('Max queue size:', maxQueueSize)
            return

        # prints best node to expand, stating g(n) and h(n)
        # and does not apply for the root node since it will always be the first to expand
        if not current_node.is_root:
            print('Best node to expand with g(n) = ', current_node.depth, ', h(n) = ', current_node.h, ', f(n) = ', current_node.f, ':', sep='')
            printPuzzle(current_node.name)
            print() # for spacing print messages

        # if goal state is not yet reached, expand tree based on the heuristic
        children = expandNode(current_node)

        # for each child from expanded node
        for child in children:
            child = Node(child, parent=current_node, h=calculateHeuristic(child, heuristic)) # adds to the tree with an attribute for its h(n)
            calculateCost(child)
            nodes.append(child) # adds to queue

        # sorts queue by heuristic in ascending order so node with the smallest f(n) is queued first
        nodes.sort(key = lambda node: node.f)

        nodesExpanded += 1 # increments counter for nodes expanded
        maxQueueSize = max(maxQueueSize, len(nodes)) # takes the maximum of the previous and current queue sizes

# main function
def main():
    start_state = selectPuzzle() # asks user which puzzle to make and makes the desired puzzle the start state
    printPuzzle(start_state) # prints selected puzzle in console
        
    algorithm = selectAlgorithm() # asks user which algorithm to use
    problem = [start_state, goal_state] # makes the problem to solve in the algorithm
    start = time.time() # start recording time

    runAlgorithm(algorithm, problem) # runs selected algorithm with the created problem

    end = time.time() # stops recording time
    print('\nTime taken:', round(end - start, 3), 'seconds') # prints how much time it took to run the search

main() # runs main function