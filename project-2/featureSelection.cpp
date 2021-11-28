#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>

struct Node {
    unsigned classification;
    std::vector<unsigned> features;
    unsigned knn_classification;
};

std::vector<Node> get_nodes(std::string filename);
std::vector<Node> knn_search(std::vector<Node> data, std::vector<unsigned> features, unsigned k);
double accuracy(std::vector<Node> data);
unsigned select_algorithm();
void forward_selection();
void backward_elimination();

int main() {
    std::cout << "Welcome to my Feature Selection Algorithm with Nearest Neighbor.\n";
    std::cout << "Enter a filename to test: ";
    std::string filename;
    std::cin >> filename;

    std::vector<Node> nodes = get_nodes(filename);
    std::cout << "\nThis dataset has " << nodes[0].features.size() << " features ";
    std::cout << "with " << nodes.size() << " instances.\n\n";

    unsigned algorithm = select_algorithm();
    if (algorithm == 1) { std::cout << "\nRunning Forward Selection...\n"; }
    else { std::cout << "\nRunning Backward Elimination...\n"; }

    return 0;
}

std::vector<Node> get_nodes(std::string filename) {
    std::vector<Node> nodes;
    std::ifstream file(filename);
    std::string line;
    if (file.is_open()) {
        while(std::getline(file, line)) {
            std::stringstream ss(line);
            std::string data;
            Node node;
            bool isClass = true;
            while (ss >> data) {
                if (isClass) {
                    node.classification = std::stoi(data);
                    isClass = false;
                }
                else {
                    node.features.push_back(std::stod(data));
                }
            }
            nodes.push_back(node);
        }
    }
    return nodes;
}

std::vector<Node> knn_search(std::vector<Node> data, std::vector<unsigned> features, unsigned k = 3) {
    std::vector<Node> nodes;
    return nodes;
}

double accuracy(std::vector<Node> data) {
    unsigned correct = 0;
    for (unsigned i = 0; i < data.size(); i++) {
        if (data[i].classification == data[i].knn_classification) { correct++; }
    }
    double result = correct / (double)data.size() * 100;
    return result;
}

unsigned select_algorithm() {
    std::cout << "Search algorithms to choose from:\n";
    std::cout << "\t1: Forward Selection\n";
    std::cout << "\t2: Backward Elimination\n\n";
    std::cout << "Choose an option: ";
    unsigned option;
    std::cin >> option;

    while (option != 1 && option != 2) {
        std::cout << "Error: Invalid option. Try again.\n";
        std::cout << "Choose an option: ";
        std::cin >> option;
    }
    return option;
}

void forward_selection() {

}

void backward_elimination() {

}