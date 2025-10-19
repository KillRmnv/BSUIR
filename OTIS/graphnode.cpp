#include "graphnode.h"

void GraphNode::updateLabelPosition() {
    if (label) {
        QRectF rect = boundingRect();
        QPointF center = rect.center();

        label->setPos(center.x() - label->boundingRect().width(),
                      rect.bottom() + 5);
    }
}
void GraphNode::mousePressEvent(QGraphicsSceneMouseEvent* event) {
    if(TOOL.getCurrentTool()==Tool::Manipulator){
    if (event->button() == Qt::LeftButton) {
        setBrush(Qt::red);
        emit nodeClicked(this);
    }
    if(event->button()==Qt::RightButton){
        QMenu contextMenu;

               QAction* actionInfo = contextMenu.addAction("Изменит идентификатор");
               QAction* actionDelete = contextMenu.addAction("Удалить");
               QAction* actionColor=contextMenu.addAction("Изменить цвет");
               QAction* actionPaths=contextMenu.addAction("Пути");
               QAction* shortestDistance=contextMenu.addAction("кратчайшее расстояние");

               QAction* selectedAction = contextMenu.exec(event->screenPos());

               if (selectedAction == actionInfo) {
                   emit changeIdentificator(this);
                          } else if (selectedAction == actionDelete) {
                          emit Delete(this);
                   QObject::disconnect(this);
                          this->deleteLater();
                      }else if(selectedAction==actionColor){
                    emit Color(this);
               }else if(selectedAction==actionPaths){
                  emit paths(this->getID());
               }else if(selectedAction==shortestDistance){
                emit shortestPath(this->getID());
               }

    }
    setCursor(Qt::ClosedHandCursor);
    dragOffset=event->pos();

    QGraphicsEllipseItem::mousePressEvent(event);
    }else if(TOOL.getCurrentTool()==Tool::ArcCreator){
        if (event->button() == Qt::LeftButton) {
            dragOffset=event->pos();
            emit Arc(this);
        }
        dragOffset=event->pos();
        QGraphicsEllipseItem::mousePressEvent(event);
    }else if(TOOL.getCurrentTool()==Tool::EdgeCreator){
        if (event->button() == Qt::LeftButton) {
            dragOffset=event->pos();
            emit Edge(this);
        }
        dragOffset=event->pos();
        QGraphicsEllipseItem::mousePressEvent(event);
    }else if(TOOL.getCurrentTool()==Tool::Delete){
        if (event->button() == Qt::LeftButton) {
            emit Delete(this);
            scene()->removeItem(this);
            emit deleteINGraph(this);
            delete this;
            return;
        }
    }
}
void GraphNode::mouseMoveEvent(QGraphicsSceneMouseEvent* event) {
    if (event->buttons() & Qt::LeftButton) {
    QPointF oldPos=pos();
    QPointF newPos = mapToParent(event->pos() - dragOffset);
           setPos(newPos);
           updateLabelPosition();
           emit moving(newPos,oldPos);
    }
    QGraphicsEllipseItem::mouseMoveEvent(event);
}
void GraphNode::mouseReleaseEvent(QGraphicsSceneMouseEvent* event) {

    setCursor(Qt::ArrowCursor);
    updateLabelPosition();
    QGraphicsEllipseItem::mouseReleaseEvent(event);
}
void GraphNode::setLabelVisible(bool visible) {
    if (label) {
        label->setVisible(visible);
    }
}
void GraphNode::setId(const QString& id) {
    if (label) {
        label->setPlainText(id);
      updateLabelPosition();
    }
}
GraphNode::GraphNode(QGraphicsItem* parent)
    : QObject(nullptr), QGraphicsEllipseItem(parent),
      label(new QGraphicsTextItem(this)),
      ID(0),
      internalCircle(nullptr) {
    setRect(-10, -10, 20, 20);
    setBrush(Qt::black);
    setPen(QPen(Qt::white, 1));
    internalCircle = new QGraphicsEllipseItem(this);
    internalCircle->setBrush(Qt::white);
    internalCircle->setPen(QPen(Qt::white, 1));
    internalCircle->setRect(-5, -5, 10, 10);
    setFlag(QGraphicsItem::ItemIsSelectable);
        setFlag(QGraphicsItem::ItemIsMovable);
        setFlag(QGraphicsItem::ItemSendsGeometryChanges);
        label->setDefaultTextColor(Qt::black);
           label->setZValue(1);
           updateLabelPosition();
           setZValue(5);
}
GraphNode::GraphNode(const QString ident, QGraphicsEllipseItem* parent,int id,QPointF xy)
    :QObject(), QGraphicsEllipseItem(parent),
      label(new QGraphicsTextItem(this)) {
    setRect(xy.x()-10, xy.y()-10, 20, 20);
    setBrush(Qt::black);
    setPen(QPen(Qt::white, 1));
    internalCircle = new QGraphicsEllipseItem(this);
    internalCircle->setBrush(Qt::white);
    internalCircle->setPen(QPen(Qt::white,1));
    internalCircle->setRect(xy.x()-5, xy.y()-5,10,10);
    ID=id;
    setFlag(QGraphicsItem::ItemIsSelectable);
        setFlag(QGraphicsItem::ItemIsMovable);
        setFlag(QGraphicsItem::ItemSendsGeometryChanges);
        label->setDefaultTextColor(Qt::black);
           label->setZValue(1);
           updateLabelPosition();
           setZValue(5);

}

void GraphNode::setNodeColor(const QColor& color) {
    setBrush(QBrush(color));
    this->color=color;
}
