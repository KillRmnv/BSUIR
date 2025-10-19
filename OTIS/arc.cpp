#include "arc.h"
#include <QPainter>
#include <QtMath>
#include <cmath>
#include<QGraphicsSceneMouseEvent>
#include <QGraphicsScene>
#include<QDebug>
void Arc::mousePressEvent(QGraphicsSceneMouseEvent* event) {
    if (event->button() == Qt::LeftButton&&TOOL.getCurrentTool()==Tool::Delete) {
        emit delet(start->getID(),end->getID());

            scene()->removeItem(this);
            delete this;
        event->accept();
    } else {
        QGraphicsItem::mousePressEvent(event);
    }
}
void Arc::Delete(GraphNode* node){
    if (!scene() ) return;
    QObject::disconnect(this);
    scene()->removeItem(this);
    emit delet(start->getID(),end->getID());
    //delete this;
     qDebug() << "Deleting Arc: ";
    this->deleteLater();
}
void Arc::changeColor(GraphNode* start,GraphNode* end,QColor color){
    if((this->start==start&&this->end==end)||(this->start==end&&this->end==start)){
        pen.setColor(color);
        update();
    }
}
void Arc::updatePosition(QPointF newPoint, QPointF oldPoint) {
    if (!scene()) return;
    Q_UNUSED(newPoint);
    Q_UNUSED(oldPoint);

    prepareGeometryChange();
    update();
}
void Arc::deleteGraphicalRepresent(GraphNode* node){
    if (!scene() ) return;
    QObject::disconnect(this);
    scene()->removeItem(this);
     this->deleteLater();
}

Arc::Arc(GraphNode* startNode, GraphNode* endNode, QGraphicsItem* parent)
    : QGraphicsItem(parent),
      start(startNode),
      end(endNode),
      pen(QPen(Qt::black, 2)),
      brush(QBrush(Qt::black)) {
    if (start && end) {
        connect(start, &GraphNode::moving, this, &Arc::updatePosition);
        connect(end, &GraphNode::moving, this, &Arc::updatePosition);
        connect(startNode,&GraphNode::Delete,this,&Arc::Delete);
        connect(endNode,&GraphNode::Delete,this,&Arc::Delete);
        connect(startNode,&GraphNode::deleteGraphicalRepresent,this,&Arc::deleteGraphicalRepresent);
        connect(endNode,&GraphNode::deleteGraphicalRepresent,this,&Arc::deleteGraphicalRepresent);

    }
    setZValue(0);

}

void Arc::setStartPoint(GraphNode* node) {
    if (start) {
        disconnect(start, &GraphNode::moving, this, &Arc::updatePosition);
    }
    start = node;
    if (start) {
        connect(start, &GraphNode::moving, this, &Arc::updatePosition);
    }
    update();
}

void Arc::setEndPoint(GraphNode* node) {
    if (end) {
        disconnect(end, &GraphNode::moving, this, &Arc::updatePosition);
    }
    end = node;
    if (end) {
        connect(end, &GraphNode::moving, this, &Arc::updatePosition);
    }
    update();
}
void Arc::setColor(const QColor& color) {
    pen.setColor(color);
    brush.setColor(color);
    update();
}
QRectF Arc::boundingRect() const {
    if (!start || !end) {
        return QRectF();
    }

    QPointF startPoint = start->mapToParent(start->boundingRect().center());
    QPointF endPoint = end->mapToParent(end->boundingRect().center());

    qreal extra = pen.widthF() / 2.0 + 10; // Учитываем толщину пера и стрелку
    return QRectF(startPoint, endPoint).normalized().adjusted(-extra, -extra, extra, extra);
}
void Arc::paint(QPainter* painter, const QStyleOptionGraphicsItem* /*option*/, QWidget* /*widget*/) {
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
    QPointF perpendicular(-unitDirection.y(), unitDirection.x());

    qreal arrowLength = 15.0;
    qreal arrowWidth = 10.0;

    QPointF arrowBase = endPoint - unitDirection * 10 - unitDirection * arrowLength;
    QPointF arrowP1 = arrowBase + perpendicular * arrowWidth / 2.0;
    QPointF arrowP2 = arrowBase - perpendicular * arrowWidth / 2.0;

    painter->drawLine(startPoint + unitDirection * 10, endPoint - unitDirection * 10);
    QPolygonF arrowHead;
    arrowHead << endPoint - unitDirection * 10 << arrowP1 << arrowP2;
    painter->drawPolygon(arrowHead);
}

