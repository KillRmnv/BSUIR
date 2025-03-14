#ifndef EDGE_INCIDENT_TO_VERTEX_ITERATOR_H
#define EDGE_INCIDENT_TO_VERTEX_ITERATOR_H

#include <iterator>
#include <vector>
#include <utility>

template<typename Vertex>
class Graph;

template<typename Vertex>
  class EdgeIncedentToVertexIterator : public std::iterator<std::bidirectional_iterator_tag, std::pair<Vertex, Vertex>> {
    private:
    typedef std::vector<std::pair<Vertex, Vertex> > EdgeList;
    typedef std::pair<Vertex, Vertex> edge;
        typename EdgeList::iterator current;
        Graph<Vertex> &graph;

    public:
        EdgeIncedentToVertexIterator(Vertex vertexToSearch,Graph<Vertex>& g);

        EdgeIncedentToVertexIterator &operator=(const EdgeIncedentToVertexIterator &other) ;

        EdgeIncedentToVertexIterator &operator++() ;

        EdgeIncedentToVertexIterator &operator--() ;

        edge &operator*() ;
        edge *operator->();
        bool operator==(const EdgeIncedentToVertexIterator &other) ;
        bool operator!=(const EdgeIncedentToVertexIterator &other);
    };
#include "EdgeIncedentIterator.cpp"
#endif
