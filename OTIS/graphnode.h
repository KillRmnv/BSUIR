#ifndef GRAPHNODE_H
#define GRAPHNODE_H

#include <QObject>
#include<QGraphicsEllipseItem>
#include <QString>
#include <QPen>
#include <QGraphicsTextItem>
#include <QGraphicsSceneMouseEvent>
#include <QBrush>
#include <QCursor>
#include <QMenu>
#include <QInputDialog>
#include<QGraphicsScene>
#include "TOOL.h"
#include "graph.h"

class GraphNode:public QObject,public QGraphicsEllipseItem
{
    Q_OBJECT
public:
    GraphNode(QGraphicsItem* parent = nullptr );
    void setNodeColor(const QColor& color);
        GraphNode(const QString ident, QGraphicsEllipseItem* parent,int id,QPointF xy);
        int getID(){
            return ID;
        }
            void setLabelVisible(bool visible);
            void setId(const QString& id);
            QColor getColor(){
                return color;
            }
            void updateLabelPosition();
            void decreaseIDByOne(){
             ID--;
            }
            QString getIdentificator(){
                return label->toPlainText();
            }
            ~GraphNode() override {
                if (label) {
                    delete label;
                    label = nullptr;
                }

                if (internalCircle) {
                    delete internalCircle;
                    internalCircle = nullptr;
                }
            }


signals:
    void nodeClicked(GraphNode* node);
    void changeIdentificator(GraphNode* node);
    void Delete(GraphNode * node);
    void deleteGraphicalRepresent(GraphNode* node);
    void Color(GraphNode* node);
    void Arc(GraphNode * node);
    void moving(QPointF xy,QPointF oldXY);
    void Edge(GraphNode * node);
    void paths(int end);
    void shortestPath(int end);
    void deleteINGraph(GraphNode * node);
private:
    int ID;
    QGraphicsEllipseItem* internalCircle;
    QPointF dragOffset;
    QGraphicsTextItem* label;
    QColor color;

protected:
    void mousePressEvent(QGraphicsSceneMouseEvent* event) override;
    void mouseMoveEvent(QGraphicsSceneMouseEvent* event) override;
    void mouseReleaseEvent(QGraphicsSceneMouseEvent* event) override;

};

#endif // NODE_H
