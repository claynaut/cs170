from anytree import Node, RenderTree
import copy

# collection of start states given by project specs from the instructor
depth_0 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
depth_2 = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
depth_4 = [[1, 2, 3], [5, 0, 6], [4, 7, 8]]
depth_8 = [[1, 3, 6], [5, 0, 2], [4, 7, 8]]
depth_12 = [[1, 3, 6], [5, 0, 7], [4, 8, 2]]
depth_16 = [[1, 6, 7], [5, 0, 3], [4, 8, 2]]
defaults = [depth_0, depth_2, depth_4, depth_8, depth_12, depth_16]

# defined goal state
goal_state = [[1, 2, 3], [4, 5 , 6], [7, 8, 0]]

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

# general search function
def search(problem, heuristic):
    root = Node(problem[0]) # set start state as the root node
    goal = Node(problem[1]) # define goal state as a node
    nodes = [root] # put root into queue
    nodesExpanded = 0
    maxQueueSize = 1

    while 1:
        # if queue is empty, search failed
        if not nodes:
            print('Failure!')
            return

        # set current node to the node at the front of the queue
        current_node = nodes.pop(0)

        # if goal state is reached, return current node
        if current_node.name == goal.name:
            print('Goal state reached!')
            print('\nSolution depth:', current_node.depth)
            print('Nodes expanded:', nodesExpanded)
            print('Max queue size:', maxQueueSize)
            return

        if not current_node.is_root:
            print('Best node to expand with g(n) =', current_node.depth, 'and h(n) =', current_node.h, 'is:')
            printPuzzle(current_node.name)
            print()

        # otherwise, expand tree based on the heuristic
        children = expandNode(current_node)
        for child in children:
            child = Node(child, parent=current_node, h=calculateHeuristic(child, heuristic))
        sortedByHeuristic = sorted(current_node.children, key = lambda child: child.h)
        nodes = nodes + sortedByHeuristic
        nodesExpanded += 1
        maxQueueSize = max(maxQueueSize, len(nodes))

def calculateHeuristic(puzzle, heuristic):
    h = 0
    if heuristic == 1:
        for row in range(len(puzzle)):
            for col in range(len(puzzle)):
                if puzzle[row][col] != goal_state[row][col] and puzzle[row][col] != 0:
                    h += 1
    elif heuristic == 2:
        misplaced = []
        for row in range(len(puzzle)):
            for col in range(len(puzzle)):
                if puzzle[row][col] != goal_state[row][col] and puzzle[row][col] != 0:
                    misplaced.append(puzzle[row][col])
        for tile in misplaced:
            [goal_row, goal_col] = getTileLocation(goal_state, tile)
            [curr_row, curr_col] = getTileLocation(puzzle, tile)
            h += abs(goal_row - curr_row) + abs(goal_col - curr_col)

    return h

def getTileLocation(puzzle, number):
    for row in range(len(puzzle)):
        if number in puzzle[row]:
            return [row, puzzle[row].index(number)]

def moveLeft(puzzle):
    [blank_row, blank_col] = getTileLocation(puzzle, 0)

    if blank_col == 0:
        return -1

    newPuzzle = copy.deepcopy(puzzle)
    newPuzzle[blank_row][blank_col] = newPuzzle[blank_row][blank_col-1]
    newPuzzle[blank_row][blank_col-1] = 0
    return newPuzzle

def moveRight(puzzle):
    [blank_row, blank_col] = getTileLocation(puzzle, 0)

    if blank_col == 2:
        return -1

    newPuzzle = copy.deepcopy(puzzle)
    newPuzzle[blank_row][blank_col] = newPuzzle[blank_row][blank_col+1]
    newPuzzle[blank_row][blank_col+1] = 0
    return newPuzzle

def moveUp(puzzle):
    [blank_row, blank_col] = getTileLocation(puzzle, 0)

    if blank_row == 0:
        return -1

    newPuzzle = copy.deepcopy(puzzle)
    newPuzzle[blank_row][blank_col] = newPuzzle[blank_row-1][blank_col]
    newPuzzle[blank_row-1][blank_col] = 0
    return newPuzzle

def moveDown(puzzle):
    [blank_row, blank_col] = getTileLocation(puzzle, 0)

    if blank_row == 2:
        return -1

    newPuzzle = copy.deepcopy(puzzle)
    newPuzzle[blank_row][blank_col] = newPuzzle[blank_row+1][blank_col]
    newPuzzle[blank_row+1][blank_col] = 0
    return newPuzzle

def expandNode(node):
    children = []
    move_left = copy.deepcopy(node.name)
    move_left = moveLeft(move_left)
    move_right = copy.deepcopy(node.name)
    move_right = moveRight(move_right)
    move_up = copy.deepcopy(node.name)
    move_up = moveUp(move_up)
    move_down = copy.deepcopy(node.name)
    move_down = moveDown(move_down)
    if move_left != -1:
        children.append(move_left)
    if move_right != -1:
        children.append(move_right)
    if move_up != -1:
        children.append(move_up)
    if move_down != -1:
        children.append(move_down)
    return children

# prints puzzle in console
def printPuzzle(puzzle):
    for row in puzzle: 
        print(row)

# main function
def main():
    # asks user which puzzle to make and makes the desired puzzle the start state
    start_state = selectPuzzle()

    # prints selected puzzle in console
    printPuzzle(start_state)
        
    # prints menu for selecting an algorithm
    algorithm = selectAlgorithm()

    # makes the problem to solve in the algorithm
    problem = [start_state, goal_state]

    # prints the start state and goal state
    print('\nStart state:')
    printPuzzle(problem[0])
    print('\nGoal state:')
    printPuzzle(problem[1])

    # starts running selected algorithm
    runAlgorithm(algorithm, problem)

# runs main function
main()