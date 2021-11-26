from anytree import Node # nodes used to create objects with custom attributes
import copy as cp # deep copy used to make a copy of a value to avoid altering a reference
import numpy as np # used for mathematical computations

# performs forward selection search
def forwardSelection(data):
    features = list(range(len(data[0].features))) # create list of features
    chosen = [[], -1] # initialize chosen features, 1st index holds features, 2nd holds accuracy
    best = [[], -1] # initialize best features, 1st index holds features, 2nd holds accuracy
    end_next_turn = -1 # used to determine when to break the while loop

    # calculate and print accuracy of all features
    print('\nRunning KNN with all features, we get an accuracy of ', round(accuracy(knnSearch(data, features)), 1), '%', sep='')

    print('\nBeginning search...\n')
    while len(features) > 0:
        accuracies = {} # use dictionary to link accuracies to specific features
        for feature in features:
            chosen[0].append(feature)
            result = knnSearch(data, chosen[0]) # get knn classification
            accuracies[feature] = accuracy(result) # calculate and store accuracy
            # note that features printed are incremented by 1 due to nature of indices in an array
            print('\tUsing feature(s) ', [i+1 for i in chosen[0]], ', accuracy is ', round(accuracies[feature], 1), '%', sep='')
            chosen[0].pop()

        if end_next_turn == 0:
            break # if flag is set to end next turn, break from while loop

        # if accuracy has decreased, send warning and toggle flag to end next turn
        if max(accuracies.values()) < chosen[1]:
            print('\nWARNING: Accuracy has decreased! Continuing search in case of local maxima...')
            end_next_turn = 0

        chosen_feature = max(accuracies, key=accuracies.get) # get key of feature with max accuracy
        chosen[0].append(chosen_feature) # add to chosen features
        chosen[1] = max(accuracies.values()) # get max accuracy from current values
        print('\nFeature(s) ', [i+1 for i in chosen[0]], ' was/were best with accuracy of ', round(max(accuracies.values()), 1), '%\n', sep='')
        
        # copy only the best set of features with highest/increasing accuracy
        if chosen[1] > best[1]:
            best = cp.deepcopy(chosen)

        features.remove(chosen_feature) # remove current feature for future searches
    
    print('\nFinished search! Best feature(s) is/are ', [i+1 for i in best[0]], ' with accuracy of ', round(best[1], 1), '%', sep='')

# prompts user for which search to run
def selectAlgorithm():
    print('\nSearch algorithms to choose from:')
    print('\t1: Forward Selection')
    print('\t2: Backward Elimination')
    option = int(input('\nChoose an option: '))
    
    # continue asking for a valid input if an invalid one was given
    while option != 1 and option != 2:
        print('Error: Invalid option. Try again.')
        option = int(input('Choose an option: '))

    # return number representing which algorithm user has chosen
    return option

# calculate accuracy of classification by k nearest neighbor
def accuracy(data):
    correct = 0
    for node in data:
        if node.classification == node.knn_classification:
            correct = correct + 1
    return correct / len(data) * 100

# performs a k nearest neighbor search algorithm, using a default k value of 5;
# note that faeturse are offset by -1 due to the nature of indices in an array
def knnSearch(data, features, k = 5):
    nodes = cp.deepcopy(data)
    for x in range(len(nodes)):
        # make an array of features to compare from test node
        a = np.array([nodes[x].features[i] for i in features])

        # make a list of neighbors excluding the test node
        neighbors = cp.deepcopy(data)
        del neighbors[x]

        # calculate the distance from test node to every other node
        for y in range(len(neighbors)):
            b = np.array([neighbors[y].features[i] for i in features])
            dist = np.linalg.norm(a-b) # uses built-in Euclidean distance algorithm
            neighbors[y].dist = dist

        # sort by smallest distances and slice array to get k neighbors
        neighbors.sort(key = lambda node: node.dist)
        neighbors = neighbors[:k]

        # count how many of each class is present in list of neighbors
        class1_cnt = 0
        class2_cnt = 0
        for n in neighbors:
            if n.classification == 1:
                class1_cnt = class1_cnt + 1
            else:
                class2_cnt = class2_cnt + 1
        
        # use majority class count to determine class of current test node
        if class1_cnt > class2_cnt:
            nodes[x].knn_classification = 1
        else:
            nodes[x].knn_classification = 2

    # return list of nodes with a new attribute of a classification determined by algorithm
    return nodes

# reads the dataset based on filename and returns a list of nodes with corresponding data
def getNodes(filename):
    cnt = 0 # used to name nodes
    nodes = []

    # open corresponding file chosen by the user
    with open(filename) as f:
        for line in f: # read each line and perform the following actions
            name = 'node' + str(cnt) # creates a unique name for each node using cnt
            node = Node(name) # intialize the node, attributes to be added
            features = []
            data = line.split() # split each line by whitespace into a list
            for i in range(len(data)):
                data[i] = float(data[i]) # convert string to float
                if i == 0: # if it's the class atrribute
                    data[i] = int(data[i]) # convert float to int
                    node.classification = data[i] # give the node the class attribute
                else:
                    features.append(data[i]) # add to a list of features to be given to the node
            node.features = features # give the node all of its features
            nodes.append(node) # add node to a list of nodes to return
            cnt = cnt + 1

    # returns a list of nodes created using the dataset
    return nodes

# main function
def main():
    print('Welcome to my Feature Selection Algorithm with Nearest Neighbor.')
    filename = input('Enter a filename to test: ')
    nodes = getNodes(filename)
    print('\nThis dataset has', len(nodes[0].features), 'features with', len(nodes), 'instances.')

    # run corresponding search chosen by the user
    algorithm = selectAlgorithm()
    if algorithm == 1:
        print('\nRunning Forward Selection...')
        forwardSelection(nodes)
    else:
        print('\nRunning Backward Elimination...')

main()