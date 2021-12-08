#include <iostream> // basic I/O
#include <fstream> // for reading the datasets
#include <sstream> // for parsing each line in the dataset
#include <string>
#include <vector>
#include <math.h> // for performing mathematical computations
#include <algorithm> // for sorting and obtaining maxima

// create struct to store information for each data point in any arbitrary dataset
struct Node {
    std::string classification; // actual class
    std::vector<double> features; // stores values of features
    double distance = -1; // Euclidean distance to be referenced (initialized to -1 for debugging purposes)
    std::string knn_classification; // class determined by k-Nearest Neighbor
};

// global variable for possible classes
std::vector<std::string> classes;

// declare functions, later defined after mamin function
std::vector<Node> get_nodes(std::string filename);
void normalize(std::vector<Node> &data);
double get_distance(Node n1, Node n2, std::vector<unsigned> f_indices);
std::vector<Node> knn_search(std::vector<Node> data, std::vector<unsigned> f_indices, unsigned k = 3);
double accuracy(std::vector<Node> data);
unsigned select_algorithm();
void print_subset(std::vector<unsigned> f_indices);
double standard_deviation(std::vector<std::pair<unsigned, double>> accuracies);
void forward_selection(std::vector<Node> data);

// main function
int main() {
    std::cout << "Welcome to my Feature Selection Algorithm with Nearest Neighbor.\n";
    // prompts user for the filename of a dataset to test
    std::cout << "Enter a filename to test: ";
    std::string filename;
    std::cin >> filename;

    std::vector<Node> nodes = get_nodes(filename); // retrieves data points
    std::cout << "\nThis dataset has " << nodes.at(0).features.size() << " features ";
    std::cout << "with " << nodes.size() << " instances.\n\n";

    normalize(nodes); // normalizes features

    // prompts user to select an algorithm and selected algorithm is then run
    unsigned algorithm = select_algorithm(); 
    if (algorithm == 1) { 
        std::cout << "\nRunning Forward Selection...\n\n";
        forward_selection(nodes);
    }

    return 0;
}

// retrieves data points within a dataset by its filename
std::vector<Node> get_nodes(std::string filename) {
    std::vector<Node> nodes; // stores data points
    std::ifstream file(filename); // opens fille by filename
    std::string line; // stores each line read in file
    if (file.is_open()) {
        while(std::getline(file, line)) { // reads file line by line
            std::stringstream ss(line); // creates a stringstream to interpret each line
            std::string data; // stores each word in each line
            Node node;
            unsigned features = 4; // used to count if features have been read for the specific dataset
            while (std::getline(ss, data, ',')) { // reads line separated by commas
                if (features == 0) {
                    // check if class exists already in a vector that keeps track of existing classes
                    bool classExists = false;
                    for (unsigned i = 0; i < classes.size(); i++) {
                        if (classes.at(i) == data) { classExists = true; }
                    }
                    // if class does not exist, add to list
                    if (!classExists) { classes.push_back(data); }
                    node.classification = data; // stores class
                    features = 4; // resets count for features
                }
                else { 
                    node.features.push_back(std::stod(data)); // stores features as doubles
                    features--; // decrements features left to read
                }
            }
            nodes.push_back(node); // adds data point to list of nodes
        }
    }
    return nodes; // returns interpreted file as a list of nodes
}

// normalizes features
void normalize(std::vector<Node> &data) {
    double f1_mean = 0.0, f2_mean = 0.0, f3_mean = 0.0, f4_mean = 0.0; // mean of each column
    double f1_std = 0.0, f2_std = 0.0, f3_std = 0.0, f4_std = 0.0; // standard deviation of each column

    // calculates the mean for each column
    // first sums up the features
    for (unsigned i = 0; i < data.size(); i++) {
        f1_mean += data.at(i).features.at(0);
        f2_mean += data.at(i).features.at(1);
        f3_mean += data.at(i).features.at(2);
        f4_mean += data.at(i).features.at(3);
    }
    // then divides by the size of the data to calculate the actual mean
    f1_mean /= data.size();
    f2_mean /= data.size();
    f3_mean /= data.size();
    f4_mean /= data.size();

    // calculates standard deviatiion in each column
    // first sums up the numerator within the standard deviation equation
    for (unsigned i = 0; i < data.size(); i++) {
        f1_std += pow(data.at(i).features.at(0) - f1_mean, 2);
        f2_std += pow(data.at(i).features.at(1) - f2_mean, 2);
        f3_std += pow(data.at(i).features.at(2) - f3_mean, 2);
        f4_std += pow(data.at(i).features.at(3) - f4_mean, 2);
    }
    // then gets the quotient standard deviation equation
    f1_std /= data.size();
    f2_std /= data.size();
    f3_std /= data.size();
    f4_std /= data.size();
    // then gets the square root to calculate the actual standard deviation
    f1_std = sqrt(f1_std);
    f2_std = sqrt(f2_std);
    f3_std = sqrt(f3_std);
    f4_std = sqrt(f4_std);

    // normalizes each feature in the dataset
    for (unsigned i = 0; i < data.size(); i++) {
        data.at(i).features.at(0) = (data.at(i).features.at(0) - f1_mean) / f1_std;
        data.at(i).features.at(1) = (data.at(i).features.at(1) - f2_mean) / f2_std;
        data.at(i).features.at(2) = (data.at(i).features.at(2) - f3_mean) / f3_std;
        data.at(i).features.at(3) = (data.at(i).features.at(3) - f4_mean) / f4_std;
    }
}

// calculates the Euclidean distances between two nodes based on a subset of features
double get_distance(Node n1, Node n2, std::vector<unsigned> f_indices) {
    std::vector<double> f1, f2; // features for n1 and n2, respectively
    // retrieves features by given indices
    for (unsigned i = 0; i < f_indices.size(); i++) {
        f1.push_back(n1.features.at(f_indices.at(i)));
        f2.push_back(n2.features.at(f_indices.at(i)));
    }

    // calculates difference and then sum the result of squaring the differences
    std::vector<double> differences;
    double sum = 0;
    for (unsigned i = 0; i < f1.size(); i++) {
        differences.push_back(f1.at(i) - f2.at(i));
        sum += pow(differences.at(i), 2);
    }
    
    double result = sqrt(sum); // calculates Euclidean distance
    return result; // returns resulting calculation
}

// performs k-Nearest Neighbor based on a set of data and a subset of features
// note that the default value of k is 3, when this function was intially declared
std::vector<Node> knn_search(std::vector<Node> data, std::vector<unsigned> f_indices, unsigned k) {
    std::vector<Node> nodes = data; // makes a copy of the original data to return at the end
    for (unsigned i = 0; i < nodes.size(); i++) {
        // copies original set of nodes except current test node so only neighbors are considered
        std::vector<Node> neighbors;
        for (unsigned j = 0; j < nodes.size(); j++) {
            if (i != j) { neighbors.push_back(nodes.at(j)); }
        }

        // calculates Euclidean distances between test node and its neighbors
        for (unsigned j = 0; j < neighbors.size(); j++) {
            neighbors.at(j).distance = get_distance(nodes.at(i), neighbors.at(j), f_indices);
        }

        // sorts by nearest neighbors and cut off by
        std::sort(neighbors.begin(), neighbors.end(), [](Node &x, Node &y){ return x.distance < y.distance; });
        neighbors.resize(k);

        // counts neighboring classes and classify test node by the majority class
        std::vector<unsigned> class_cnt; // uses vector to keep count of each class
        for (unsigned j = 0; j < classes.size(); j++) {
            class_cnt.push_back(0); // initialize each count to 0
        }
        for (unsigned j = 0; j < neighbors.size(); j++) {
            // increment count for specific class it matches
            for (unsigned k = 0; k < classes.size(); k++) {
                if (neighbors.at(j).classification == classes.at(k)) { class_cnt.at(k)++; }
            }
        }
        // gets index of highest class count
        // referenced stack overflow [https://stackoverflow.com/questions/2953491/finding-the-position-of-the-maximum-element]
        auto majority_index = std::distance(class_cnt.begin(), std::max_element(class_cnt.begin(), class_cnt.end()));
        nodes.at(i).knn_classification = classes.at(majority_index);
    }
    return nodes; // returns list of nodes with updated predicted class attributes
}

// calculates accuracy of predicted classifications by k-Nearest Neighbor
double accuracy(std::vector<Node> data) {
    unsigned correct = 0;
    double result = 0.0;
    // counts how many nodes were correctly classified by comparing actual/predicted class attributes
    for (unsigned i = 0; i < data.size(); i++) {
        if (data.at(i).classification == data.at(i).knn_classification) { correct++; }
    }
    result = correct / (double)data.size() * 100; // calculates percentage
    return result; // returns percentage
}

// prompts user to select an algorithm to run
unsigned select_algorithm() {
    std::cout << "Search algorithms to choose from:\n";
    std::cout << "\t1: Forward Selection\n\n";
    // prompts user to choose an option from the above menu
    std::cout << "Choose an option: ";
    unsigned option;
    std::cin >> option;

    // if user inputs invalid option, it continues to prompt user until a valid one is entered
    while (option != 1) {
        std::cout << "Error: Invalid option. Try again.\n";
        std::cout << "Choose an option: ";
        std::cin >> option;
    }
    return option; // returns number corresponding to chosen algorithm
}

// prints subset of features into console
void print_subset(std::vector<unsigned> f_indices) {
    std::cout << "{";
    for (unsigned i = 0; i < f_indices.size(); i++) {
        std::cout << f_indices.at(i)+1; // indices are incremented by 1 due to indices starting from 0
        // only prints commas if last index has not been reached yet
        if (i != f_indices.size()-1) { std::cout << ", "; }
    }
    std::cout << "}";
}

// performs Forward Selection on given set of data points, starting with no features
void forward_selection(std::vector<Node> data) {
    // creates a vector filled with possible features by index
    std::vector<unsigned> features;
    for (unsigned i = 0; i < data.at(0).features.size(); i++) { features.push_back(i); }
    // initializes subsets to store current subset being tested and the best subset so far
    // note that the start state is a subset with no features
    std::pair<std::vector<unsigned>, double> chosenSubset;
    chosenSubset.first = {};
    chosenSubset.second = accuracy(knn_search(data, {}));
    std::pair<std::vector<unsigned>, double> bestSubset;
    bestSubset.first = {};
    bestSubset.second = accuracy(knn_search(data, {}));
    bool accuracyDecreased = false; // used to determine when to end the search

    std::cout.precision(1); // sets to one decimal place
    std::cout << std::fixed; // fixes following number outputs within this function to follow set precision

    // shows results from running k-Nearest Neighbor using all/no features
    std::cout << "\tRunning KNN with ALL features, we get an accuracy of ";
    std::cout << accuracy(knn_search(data, features)) << "%\n";
    std::cout << "\tRunning KNN with NO features, we get an accuracy of ";
    std::cout << accuracy(knn_search(data, {})) << "%\n\n";

    std::cout << "Beginning search...\n\n";
    while (features.size() > 0) {
        // vector used to store subsets of features with their corresponding accuracy
        std::vector<std::pair<unsigned, double>> accuracies;
        for (unsigned i = 0; i < features.size(); i++) {
            chosenSubset.first.push_back(features.at(i)); // adds feature to test
            // performs k-Nearest Neighbor to classify dataset by current feature subset
            std::vector<Node> result = knn_search(data, chosenSubset.first);
            // calculates accuracy and adds to list of existing accuracies to compare later
            accuracies.push_back(std::make_pair(features.at(i), accuracy(result)));

            // prints resulting accuracy from tested feature subset
            std::cout << "\tUsing feature(s) ";
            print_subset(chosenSubset.first);
            std::cout << ", accuracy is " << accuracy(knn_search(data, chosenSubset.first)) << "%\n";
            chosenSubset.first.pop_back(); // removes tested feature
        }

        // gets pair with the highest accuracy
        // referenced stack overflow [https://stackoverflow.com/questions/56745759/how-to-find-max-value-of-second-element-of-stdpair-in-stdvector]
        auto maxAccuracy = std::max_element(accuracies.begin(), accuracies.end(), [](std::pair<unsigned, double> &x, std::pair<unsigned, double> &y){ return x.second < y.second; });

        // ends search when accuracy has decreased previously and accuracy seems to not improve
        if (accuracyDecreased && maxAccuracy->second < bestSubset.second) { break; }

        // if recently calculated best accuracy is less than the previous best,
        // toggles flag that accuracy has decreased and warns the user
        if (maxAccuracy->second < chosenSubset.second) {
            std::cout << "\nWARNING: Accuracy has decreased! Continuing search in case of local maxima...\n";
            accuracyDecreased = true;
        }

        chosenSubset.first.push_back(maxAccuracy->first); // adds the best feature to existing chosen
        chosenSubset.second = maxAccuracy->second; // updates accuracy
        // outputs to the user the result of current search
        std::cout << "\nFeature subset ";
        print_subset(chosenSubset.first);
        std::cout << " is the best with accuracy of " << maxAccuracy->second << "%\n\n";

        // if current subset is better than previously logged best subset, update the best subset
        if (chosenSubset.second > bestSubset.second) { bestSubset = chosenSubset; }

        // removes chosen feature from features to be tested in future/remaining searches
        // referenced https://stackoverflow.com/questions/19807783/how-to-copy-a-vector-except-one-specific-element
        features.erase(std::find(features.begin(), features.end(), maxAccuracy->first));
    }
    // outputs best results in the end
    std::cout << "\nFinished search! Best feature subset is ";
    print_subset(bestSubset.first);
    std::cout << " with accuracy of " << bestSubset.second << "%\n";
}
