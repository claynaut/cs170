def makePuzzle(option):
    if (option == 1):
        print('\nUsing default puzzle layout...')
        return [[1, 2, 3], [4, 5 , 6], [7, 8, 0]]
    elif (option == 2):
        print('\nCreating custom puzzle layout...')
        possible_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        available_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        row1 = []
        row2 = []
        row3 = []

        print('Enter the first row:')
        for i in range(3):
            element = int(input())
            while (not (element in possible_numbers)):
                print('Error: Invalid input. Select numbers from 0-8.')
                element = int(input())
            while (not (element in available_numbers)):
                print('Error: Duplicate value. Number already added to puzzle.')
                element = int(input())
            available_numbers[available_numbers.index(element)] = -1
            row1.append(element)

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

        return [row1, row2, row3]
    else:
        return -1;

def printMenu():
    print('Welcome to my 8-puzzle solver!')
    print('\t1. Use default puzzle layout')
    print('\t2. Create a custom puzzle layout')

def main():
    printMenu()
    option  = int(input('\nChoose an option: '))

    puzzle = makePuzzle(option)
    while (puzzle == -1):
        print('Error: Invalid option. Try again.')
        option  = int(input('Choose an option: '))
        puzzle = makePuzzle(option)

    for row in puzzle:
        print(row)
        
    print('\nSelect algorithm.')
    print('\t1. Uniform Cost Search')
    print('\t2. Misplaced Tile heuristic')
    print('\t2. Manhattan Distance heuristic')

main()