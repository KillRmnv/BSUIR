#ifndef GRAPH_H
#define GRAPH_H


#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <unordered_set>
#include<map>
#include<gtest/gtest.h>
#include "EdgeIterator.h"
#include "VertexIterator.h"
#include "EdgeIncedentIterator.h"

template<typename Vertex>
class Graph {
private:
    typedef std::map<Vertex, int> VertexMap;
    std::vector<std::pair<Vertex, Vertex> > edges;
    VertexMap vertices;

public:
    typedef std::vector<std::pair<Vertex, Vertex> > EdgeList;
    typedef std::pair<Vertex, Vertex> edge;
    typedef edge &EdgeLink;
    typedef edge *EdgePointer;
    typedef typename EdgeList::iterator iterator;
    typedef typename VertexMap::iterator vertex_iterator;

    Graph() = default;

    ~Graph() = default;

    size_t vertexCount() const {
        return vertices.size();
    }

    size_t edgeCount() const {
        return edges.size();
    }



   Graph(Vertex vertex, Vertex vertex2) {
        edges.push_back({vertex, vertex2});
    }

  Graph( Graph &other) {
        for (auto edge: other.getEdges()) {
            edges.push_back(edge);
        }
    }


    bool empty() const { return edges.empty(); }

    void clear() { edges.clear(); vertices.clear(); }

    Graph<Vertex>& operator=(const Graph &other) {
        if (this != &other) {
            edges = other.edges;
        }
        return *this;
    }


     friend std::ostream& operator<<(std::ostream &os, const Graph<Vertex> &graph) {
        std::for_each(graph.edges.begin(), graph.edges.end(),
                      [&os](const  EdgeList &edge) {
                          os << edge.first << " -> " << edge.second << "\n";
                      });
        return os;
    }

    std::vector<std::pair<Vertex, Vertex> >& getEdges() {
        return edges;
    }

    void addEdge(Vertex vertex1, Vertex vertex2) {
        if (vertex1 != vertex2) {
            edges.push_back({vertex1, vertex2});
            sort();
            if (vertices.find(vertex1) == vertices.end()) {
                vertices[vertex1] = 1;
            } else {
                vertices[vertex1] += 1;
            }
        } else {
            throw std::invalid_argument("Edge can be added only between different vertices ");
        }
    }

    void sort() {
        std::sort(edges.begin(), edges.end());
    }

    void removeEdge(const edge &Edge) {
        auto it = std::find(edges.begin(), edges.end(), Edge);
        if (it != edges.end()) {
            edges.erase(it);
            vertices[it->first]--;
        } else {
            throw std::invalid_argument("Edge not found");
        }
    }

    bool operator==(const Graph &other) const {
        return edges == other.edges;
    }

    bool operator!=(const Graph &other) const {
        return !(*this == other);
    }

    bool operator<(const Graph &other) const {
        return edges < other.edges;
    }

    bool operator>(const Graph &other) const {
        return edges > other.edges;
    }

    bool operator<=(const Graph &other) const {
        return edges <= other.edges;
    }

    bool operator>=(const Graph &other) const {
        return edges >= other.edges;
    }

    bool checkVertexExistance(Vertex vertex) {
        return vertices.find(vertex) != vertices.end();
    }

    bool edgeExists(edge checkEdge) {
        return findEdge(checkEdge) != edges.end();
    }

    int vertexDegree(Vertex vertex) {
        if (vertices.find(vertex) == vertices.end()) {
            throw std::invalid_argument("Vertex does not exist");
        }
        return vertices[vertex];
    }

    int edgeDegree(edge checkEdge) {
        if (findEdge(checkEdge) == edges.end()) {
            throw std::invalid_argument("Edge does not exist");
        }
        return vertices[checkEdge.first] * vertices[checkEdge.second];
    }

    int findVertex(Vertex vertex) {
        if (vertices.find(vertex) == vertices.end()) {
            throw std::invalid_argument("Vertex does not exist");
        }
        int left = 0, right = edges.size() - 1, mid = (left + right) / 2;
        while (left < right) {
            if (edges[mid].first > vertex) {
                left = mid;
            } else if (edges[mid].first < vertex) {
                right = mid;
            } else if (edges[mid].first == vertex) {
                for (; edges[mid].first == vertex && mid > -1; --mid) {
                }
                ++mid;
                return mid;
            }
        }
        if (edges[mid].first == vertex) {
            return mid;
        }
        throw std::invalid_argument("Vertex does not exist");
    }

    void removeVertex(Vertex vertex) {
        if (vertices.find(vertex) == vertices.end()) {
            throw std::invalid_argument("Vertex does not exist");
        }
        if (vertices[vertex] != 0) {
            int mid = findVertex(vertex);
            for (; edges[mid].first == vertex && mid < edges.size();) {
                edges.erase(edges.begin() + mid);
            }
        }
        vertices.erase(vertex);
    }

    void addVertex(Vertex vertex) {
        if (vertices.find(vertex) == vertices.end()) {
            vertices[vertex] = 0;
        } else {
            throw std::invalid_argument("Vertex already exists");
        }
    }

typename std::vector<std::pair<Vertex, Vertex> > ::iterator  beginEdges() { return edges.begin(); }

typename std::vector<std::pair<Vertex, Vertex> > ::iterator  endEdges() { return edges.end(); }

typename std::vector<std::pair<Vertex, Vertex> > ::iterator  findEdge(const edge &Edge) {
    return std::find(edges.begin(), edges.end(), Edge);
}

std::map<Vertex,int> getVertexSet() {
    return vertices;
}

void removeVertex(IncedentVertexIterator<Vertex> it) {
    Vertex vertex = *it;
    removeVertex(vertex);
}

void removeEdge(EdgeIncedentToVertexIterator<Vertex> it) {
    removeEdge(it->first, it->second);
}

void removeEdge(iterator it) {
    removeEdge({it->first, it->second});
}

void removeEdge(EdgeIterator<Vertex> it) {
    removeEdge({it->first, it->second});
}

typename std::vector<std::pair<Vertex, Vertex> >::const_reverse_iterator rbeginEdges() const { return edges.rbegin(); }

typename std::vector<std::pair<Vertex, Vertex> >::const_reverse_iterator rendEdges() const { return edges.rend(); }

typename std::vector<std::pair<Vertex, Vertex> >::const_iterator beginEdges() const { return edges.begin(); }

typename std::vector<std::pair<Vertex, Vertex> >::const_iterator endEdges() const { return edges.end(); }

};
#endif
