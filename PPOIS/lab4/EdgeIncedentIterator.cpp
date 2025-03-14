#ifndef EDGE_INCIDENT_TO_VERTEX_ITERATOR_CPP
#define EDGE_INCIDENT_TO_VERTEX_ITERATOR_CPP

#include "EdgeIncedentIterator.h"
#include "Graph.h" // Для использования класса Graph

template<typename Vertex>
EdgeIncedentToVertexIterator<Vertex>::EdgeIncedentToVertexIterator(Vertex vertexToSearch, Graph<Vertex> &g)
        : graph(g) {
    auto temp = graph.getEdges()[graph.findVertex(vertexToSearch)];
    current = graph.findEdge(temp);
}

template<typename Vertex>
EdgeIncedentToVertexIterator<Vertex> &EdgeIncedentToVertexIterator<Vertex>::operator=(const EdgeIncedentToVertexIterator &other) {
    current = other.current;
    return *this;
}

template<typename Vertex>
EdgeIncedentToVertexIterator<Vertex> &EdgeIncedentToVertexIterator<Vertex>::operator++() {
    auto temp = *current;
    ++current;
    if (current->first == temp.first) {
        return *this;
    } else {
        for (auto vert: graph.getVertexSet()) {
            for (int index = graph.findVertex(vert.first); graph.getEdges()[index].first == vert.first; ++index) {
                if (temp.first == graph.getEdges()[index].second && graph.getEdges()[index].first > temp.first) {
                    current = graph.findEdge(temp);
                    return *this;
                }
                if (graph.getEdges()[index].first < graph.getEdges()[index].second) {
                    break;
                }
            }
        }
    }
    return *this;
}

template<typename Vertex>
EdgeIncedentToVertexIterator<Vertex> &EdgeIncedentToVertexIterator<Vertex>::operator--() {
    auto temp = *current;
    --current;
    if (current->first == temp.first) {
        return *this;
    } else {
        auto it = graph.findEdge(temp);
        --it;
        for (; it != graph.beginEdges(); --it) {
            if (temp.first == it->second || temp.first == it->first) {
                current->first = it->first;
                current->second = it->second;
                return *this;
            }
        }
    }
    return *this;
}

template<typename Vertex>
std::pair<Vertex, Vertex> &EdgeIncedentToVertexIterator<Vertex>::operator*() {
    return *current;
}

template<typename Vertex>
std::pair<Vertex, Vertex> *EdgeIncedentToVertexIterator<Vertex>::operator->() {
    return &(*current);
}

template<typename Vertex>
bool EdgeIncedentToVertexIterator<Vertex>::operator==(const EdgeIncedentToVertexIterator &other)  {
    return current == other.current;
}

template<typename Vertex>
bool EdgeIncedentToVertexIterator<Vertex>::operator!=(const EdgeIncedentToVertexIterator &other)  {
    return current != other.current;
}

#endif // EDGE_INCIDENT_TO_VERTEX_ITERATOR_CPP
