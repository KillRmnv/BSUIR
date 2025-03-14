#ifndef EDGE_ITERATOR_H
#define EDGE_ITERATOR_H

#include <iterator>
#include <vector>
#include <utility>

template<typename Vertex>
class Graph;

template<typename Vertex>
class EdgeIterator : public std::iterator<std::bidirectional_iterator_tag,  std::pair<Vertex, Vertex>> {
private:
    typedef std::vector<std::pair<Vertex, Vertex> > EdgeList;
    typedef std::pair<Vertex, Vertex> edge;
    typename EdgeList::iterator current;

public:

  explicit EdgeIterator(typename EdgeList::iterator it)  {
current = it;}
    EdgeIterator &operator=(const EdgeIterator &other) ;

    bool operator==(const EdgeIterator &other);

    bool operator!=(const EdgeIterator &other);

    EdgeIterator &operator++() ;
    EdgeIterator operator++(int);
    EdgeIterator &operator--() ;
    EdgeIterator operator--(int);

    edge &operator*() ;
    edge *operator->() ;
};
#include "EdgeIterator.cpp"
#endif
