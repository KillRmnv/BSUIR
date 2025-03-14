#ifndef INCEDENT_VERTEX_ITERATOR_H
#define INCEDENT_VERTEX_ITERATOR_H

#include <iterator>
#include <vector>
#include <utility>

template<typename Vertex>
class Graph;

template<typename Vertex>
class IncedentVertexIterator : public std::iterator<std::bidirectional_iterator_tag, Vertex> {
private:
    typename std::vector<std::pair<Vertex, Vertex>>::iterator current;

public:
    IncedentVertexIterator(Vertex vertexToSearch, Graph<Vertex> &graph);
    IncedentVertexIterator &operator=(const IncedentVertexIterator &other);
    IncedentVertexIterator &operator++();    // Префиксный
    IncedentVertexIterator operator++(int); // Постфиксный
    IncedentVertexIterator &operator--();
    IncedentVertexIterator operator--(int);

    Vertex &operator*();
    Vertex *operator->();

    bool operator==(const IncedentVertexIterator &other) const;
    bool operator!=(const IncedentVertexIterator &other) const;
};

#include "VertexIterator.cpp"

#endif
