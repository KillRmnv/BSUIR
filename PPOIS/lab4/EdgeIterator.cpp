#ifndef EDGE_ITERATOR_CPP
#define EDGE_ITERATOR_CPP

#include "EdgeIterator.h"
#include "Graph.h"

template<typename Vertex>
EdgeIterator<Vertex> &EdgeIterator<Vertex>::operator=(const EdgeIterator &other) {
    current = other.current;
    return *this;
}

template<typename Vertex>
bool EdgeIterator<Vertex>::operator==(const EdgeIterator &other)  {
    return current == other.current;
}

template<typename Vertex>
bool EdgeIterator<Vertex>::operator!=(const EdgeIterator &other)  {
    return current != other.current;
}

template<typename Vertex>
EdgeIterator<Vertex> &EdgeIterator<Vertex>::operator++() {
    ++current;
    return *this;
}

template<typename Vertex>
EdgeIterator<Vertex> EdgeIterator<Vertex>::operator++(int) {
    EdgeIterator temp = *this;
    ++current;
    return temp;
}

template<typename Vertex>
EdgeIterator<Vertex> &EdgeIterator<Vertex>::operator--() {
    --current;
    return *this;
}

template<typename Vertex>
EdgeIterator<Vertex> EdgeIterator<Vertex>::operator--(int) {
    EdgeIterator temp = *this;
    --current;
    return temp;
}

template<typename Vertex>
std::pair<Vertex, Vertex> &EdgeIterator<Vertex>::operator*() {
    return *current;
}

template<typename Vertex>
std::pair<Vertex, Vertex> *EdgeIterator<Vertex>::operator->() {
    return &(*current);
}

#endif
