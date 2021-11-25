from anytree import Node # nodes used to create objects with custom attributes
import copy as cp # deep copy used to make a copy of a value to avoid altering a reference
import numpy as np

# calculate accuracy of classification by k nearest neighbor
def accuracy(data):
    accuracy = 0
    for node in data:
        if node.classification == node.knnclassification:
            accuracy = accuracy + 1
    return (accuracy / len(data))

# performs a k nearest neighbor search algorithm, using a default k value of 5
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
            nodes[x].knnclassification = 1
        else:
            nodes[x].knnclassification = 2

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
                    features.append(data[i]) # add to a list of features to be given to the node at the end
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
    
main()