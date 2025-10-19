#ifndef ARC_H
#define ARC_H

#include <QObject>
#include <QGraphicsItem>
#include <QPen>
#include <QBrush>
#include "TOOL.h"
#include "graphnode.h"

class Arc : public QObject, public QGraphicsItem {
    Q_OBJECT
   signals:
    void delet(int first, int second);

public:
    explicit Arc(GraphNode* startNode, GraphNode* endNode, QGraphicsItem* parent);
    ~Arc() override = default;

    void setStartPoint(GraphNode* node);
    void setEndPoint(GraphNode* node);
    void setColor(const QColor& color);
    QColor getColor() const { return pen.color(); }

public slots:
    void updatePosition(QPointF newPoint, QPointF oldPoint);
    void Delete(GraphNode* node);
    void deleteGraphicalRepresent(GraphNode* node);
    void changeColor(GraphNode* start,GraphNode* end,QColor qolor);

protected:
    QRectF boundingRect() const override; // Область отрисовки
    void paint(QPainter* painter, const QStyleOptionGraphicsItem* option, QWidget* widget) override;
    void mousePressEvent(QGraphicsSceneMouseEvent* event) override;

protected:
    GraphNode* start;
    GraphNode* end;
    QPen pen;
    QBrush brush;
};

#endif // ARC_H
