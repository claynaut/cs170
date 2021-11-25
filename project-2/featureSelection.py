from anytree import Node # nodes used to create objects with custom attributes
import copy # deep copy used to make a copy of a value to avoid altering a reference

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