#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <math.h>
#include <algorithm>

struct Node {
    unsigned classification;
    std::vector<double> features;
    double distance = -1;
    unsigned knn_classification;
};

std::vector<Node> get_nodes(std::string filename);
double get_distance(Node n1, Node n2, std::vector<unsigned> f_indices);
std::vector<Node> knn_search(std::vector<Node> data, std::vector<unsigned> f_indices, unsigned k);
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
    std::cout << "\nThis dataset has " << nodes.at(0).features.size() << " features ";
    std::cout << "with " << nodes.size() << " instances.\n\n";

    // unsigned algorithm = select_algorithm();
    // if (algorithm == 1) { std::cout << "\nRunning Forward Selection...\n"; }
    // else { std::cout << "\nRunning Backward Elimination...\n"; }

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
                else { node.features.push_back(std::stod(data)); }
            }
            nodes.push_back(node);
        }
    }
    return nodes;
}

double get_distance(Node n1, Node n2, std::vector<unsigned> f_indices) {
    std::vector<double> f1;
    std::vector<double> f2;
    for (unsigned i = 0; i < f_indices.size(); i++) {
        f1.push_back(n1.features.at(f_indices.at(i)));
        f2.push_back(n2.features.at(f_indices.at(i)));
    }

    std::vector<double> differences;
    double sum = 0;
    for (unsigned i = 0; i < f1.size(); i++) {
        differences.push_back(f1.at(i) - f2.at(i));
        sum += pow(differences.at(i), 2);
    }
    
    double result = sqrt(sum);
    return result;
}

std::vector<Node> knn_search(std::vector<Node> data, std::vector<unsigned> f_indices, unsigned k) {
    std::vector<Node> nodes = data;
    for (unsigned i = 0; i < nodes.size(); i++) {
        std::vector<Node> neighbors;
        for (unsigned j = 0; j < nodes.size(); j++) {
            if (i != j) { neighbors.push_back(nodes.at(j)); }
        }

        for (unsigned j = 0; j < neighbors.size(); j++) {
            neighbors.at(j).distance = get_distance(nodes.at(i), neighbors.at(j), f_indices);
        }

        std::sort(neighbors.begin(), neighbors.end(), [](Node &x, Node &y){ return x.distance < y.distance; });
        neighbors.resize(k);

        unsigned c1_cnt = 0;
        unsigned c2_cnt = 0;
        for (unsigned j = 0; j < neighbors.size(); j++) {
            if (neighbors.at(j).classification == 1) { c1_cnt++; }
            else { c2_cnt++; }
        }

        if (c1_cnt > c2_cnt) { nodes.at(i).knn_classification = 1; }
        else { nodes.at(i).knn_classification = 2; }
    }
    return nodes;
}

double accuracy(std::vector<Node> data) {
    unsigned correct = 0;
    for (unsigned i = 0; i < data.size(); i++) {
        if (data.at(i).classification == data.at(i).knn_classification) { correct++; }
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