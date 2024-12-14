#ifndef INCEDENT_VERTEX_ITERATOR_CPP
#define INCEDENT_VERTEX_ITERATOR_CPP

#include "VertexIterator.h"
#include "Graph.h"

template<typename Vertex>
IncedentVertexIterator<Vertex>::IncedentVertexIterator(Vertex vertexToSearch, Graph<Vertex> &graph) {
    current = graph.findEdge(graph.getEdges()[graph.findVertex(vertexToSearch)]);
}

template<typename Vertex>
IncedentVertexIterator<Vertex> &IncedentVertexIterator<Vertex>::operator=(const IncedentVertexIterator &other) {
    current = other.current;
    return *this;
}

template<typename Vertex>
IncedentVertexIterator<Vertex> &IncedentVertexIterator<Vertex>::operator++() {
    ++current;
    return *this;
}

template<typename Vertex>
IncedentVertexIterator<Vertex> IncedentVertexIterator<Vertex>::operator++(int) {
    IncedentVertexIterator temp = *this;
    ++current;
    return temp;
}

template<typename Vertex>
IncedentVertexIterator<Vertex> &IncedentVertexIterator<Vertex>::operator--() {
    --current;
    return *this;
}

template<typename Vertex>
IncedentVertexIterator<Vertex> IncedentVertexIterator<Vertex>::operator--(int) {
    IncedentVertexIterator temp = *this;
    --current;
    return temp;
}

template<typename Vertex>
Vertex &IncedentVertexIterator<Vertex>::operator*() {
    return current->second;
}

template<typename Vertex>
Vertex *IncedentVertexIterator<Vertex>::operator->() {
    return &current->second;
}

template<typename Vertex>
bool IncedentVertexIterator<Vertex>::operator==(const IncedentVertexIterator &other) const {
    return current == other.current;
}

template<typename Vertex>
bool IncedentVertexIterator<Vertex>::operator!=(const IncedentVertexIterator &other) const {
    return current != other.current;
}

#endif
