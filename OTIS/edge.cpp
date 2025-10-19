#include "edge.h"
#include <QPainter>
#include <QtMath>
#include <cmath>
Edge::Edge(GraphNode* startNode, GraphNode* endNode, QGraphicsItem* parent)
    : Arc(startNode,endNode,parent) {
    start = startNode;
    end = endNode;

    if (start && end) {
        connect(start, &GraphNode::moving, this, &Arc::updatePosition);
        connect(end, &GraphNode::moving, this, &Arc::updatePosition);
    }
}
void Edge::paint(QPainter* painter, const QStyleOptionGraphicsItem* /*option*/, QWidget* /*widget*/) {
    if (!start || !end) {
        return;
    }

    QPointF startPoint = start->mapToScene(start->boundingRect().center());
    QPointF endPoint = end->mapToScene(end->boundingRect().center());

    painter->setPen(pen);
    painter->setBrush(brush);

    QPointF direction = endPoint - startPoint;
    qreal length = std::sqrt(direction.x() * direction.x() + direction.y() * direction.y());
    if (length == 0.0) return;

    QPointF unitDirection = direction / length;

    painter->drawLine(startPoint + unitDirection * 10, endPoint - unitDirection * 10);

}
QRectF Edge::boundingRect() const {
    if (!start || !end) {
        return QRectF();
    }

    QPointF startPoint = start->mapToParent(start->boundingRect().center());
    QPointF endPoint = end->mapToParent(end->boundingRect().center());

    qreal extra = pen.widthF() / 2.0; // Учитываем толщину пера и стрелку
    return QRectF(startPoint, endPoint).normalized().adjusted(-extra, -extra, extra, extra);
}
