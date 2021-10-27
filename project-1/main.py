# creates an 8-puzzle based on the user's option and returns the generated 8-puzzle
def selectPuzzle():
    print('Select a puzzle to solve for this 8-puzzle solver.')
    print('\t1. Use default puzzle layout')
    print('\t2. Create a custom puzzle layout')

    # retrieves user's selection for which puzzle to make
    option  = int(input('\nChoose an option: '))

    # if user selects an invalid option, loop until a valid input is made
    while (option != 1 and option != 2):
        print('Error: Invalid option. Try again.')
        option  = int(input('Choose an option: '))

    # returns default puzzle layout
    if (option == 1):
        print('\nUsing default puzzle layout...')

        # returns default puzzle
        return [[1, 2, 3], [4, 5 , 6], [7, 8, 0]]

    # creates a custom puzzle layout
    elif (option == 2):
        print('\nCreating custom puzzle layout...')
        # array used to validate user input (user must input only numbers 0-8)
        possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        # array used to validate user input (checked to make sure user doesn't input duplicate numbers)
        # each element is set to -1 to indicate the number is already taken
        available_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        row1 = [] # first row of the puzzle
        row2 = [] # second row of the puzzle
        row3 = [] # third row of the puzzle

        # creates first row of the puzzle
        print('Enter the first row:')
        # for loop ran 3 times for 3 numbers in a row
        for i in range(3):
            # retrieves user's input for a number in the row
            element = int(input())

            # check if the number selected is in the possible numbers to select from
            # otherwise, loop until the user inputs a valid number
            while (not (element in possible_numbers)):
                print('Error: Invalid input. Select numbers from 0-8.')
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
            row1.append(element)

        # creates second row of the puzzle
        print('Enter the second row:')
        for i in range(3):
            element = int(input())
            while (not (element in possible_numbers)):
                print('Error: Invalid input. Select numbers from 0-8.')
                element = int(input())
            while (not (element in available_numbers)):
                print('Error: Duplicate value. Number already added to puzzle.')
                element = int(input())
            available_numbers[available_numbers.index(element)] = -1
            row2.append(element)

        # creates third row of the puzzle
        print('Enter the third row:')
        for i in range(3):
            element = int(input())
            while (not (element in possible_numbers)):
                print('Error: Invalid input. Select numbers from 0-8.')
                element = int(input())
            while (not (element in available_numbers)):
                print('Error: Duplicate value. Number already added to puzzle.')
                element = int(input())
            available_numbers[available_numbers.index(element)] = -1
            row3.append(element)

        # returns user-created puzzle
        return [row1, row2, row3]

# asks user which algorithm to use and returns a number indicating which algorithm to use
def selectAlgorithm():
    print('\nSelect algorithm.')
    print('\t1. Uniform Cost Search')
    print('\t2. A* with Misplaced Tile heuristic')
    print('\t2. A* Manhattan Distance heuristic')

    # retrieves user's selection on which algorithm to use
    option  = int(input('\nChoose an option: '))

    # if user selects an invalid option, loop until a valid input is made
    while (option != 1 and option != 2 and option != 3):
        print('Error: Invalid option. Try again.')
        option  = int(input('Choose an option: '))

    # returns user's selection
    return option

# prints out which algorithm will be used and calls the respective function for that algorithm
def runAlgorithm(option):
    # runs algorithm for uniform cost search
    if (option == 1):
        print('\nSolving with Uniform Cost Search...')

    # runs algorithm for A* with misplaced tile heuristic
    elif (option == 2):
        print('\Solving with A* with Misplaced Tile heuristic...')

    # runs algorithm for A* with manhattan distance heuristic
    elif (option == 3):
        print('\Solving with A* Manhattan Distance heuristic...')

# prints puzzle in console
def printPuzzle(puzzle):
    for row in puzzle: 
        print(row)

# main function
def main():
    # asks user which puzzle to make and makes the desired puzzle
    puzzle = selectPuzzle()

    # prints selected puzzle in console
    printPuzzle(puzzle)
        
    # prints menu for selecting an algorithm
    algorithm = selectAlgorithm()

    # starts running selected algorithm
    runAlgorithm(algorithm)

# runs main function
main()