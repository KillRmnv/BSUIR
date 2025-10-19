#ifndef EDGE_H
#define EDGE_H


#include "arc.h"
class Edge : public Arc {
    Q_OBJECT
public:
    explicit Edge(GraphNode* startNode, GraphNode* endNode, QGraphicsItem* parent);
    ~Edge() override = default;
protected:
    QRectF boundingRect() const override; // Область отрисовки
    void paint(QPainter* painter, const QStyleOptionGraphicsItem* option, QWidget* widget) override;

};

#endif // EDGE_H
