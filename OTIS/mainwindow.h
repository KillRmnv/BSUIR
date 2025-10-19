#ifndef MAINWINDOW_H
#define MAINWINDOW_H
#include<QApplication>
#include <QMainWindow>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QMouseEvent>
#include <QVector>
#include <QToolBar>
#include <QAction>
#include <QMenu>
#include <QTabWidget>
#include <QWidget>
#include <QInputDialog>
#include<QTextEdit>
#include<QVBoxLayout>
#include<QDialog>
#include<QColorDialog>
#include "graphnode.h"
#include "edge.h"
#include <QDialog>
#include <QPushButton>
#include <QVBoxLayout>
#include <QLabel>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class Tab:public QTabWidget{
    Q_OBJECT
private:

    GraphNode* currentNode;

    QVector<GraphNode*> Nodes;

    QGraphicsScene* scene;

    QGraphicsView* view;

    void mouseDoubleClickEvent(QMouseEvent *event);

    void mousePressEvent(QMouseEvent *event);

    Graph graph;

    void showNextCycleNotification(QGraphicsScene* scene,  std::vector<std::vector<unsigned int>>& cycles, int& currentIndex);

    void keyPressEvent(QKeyEvent* event);

private slots:

    void CreateNode(QPointF xy);

    void CreateArc(GraphNode* node);

    void CreateEdge(GraphNode* node);

    void nodeDelete(GraphNode* node);

    void deleteArc(int start,int end);

    void deleteEdge(int start,int end);

    void findPaths(int end);

    void shortest(int end);
public slots:
    void InfoAboutgraph();
    void setCurrentNode(GraphNode* node);
    void inputDialog(GraphNode* node);
    void changeColor(GraphNode* node);
signals:
    void EsckeyPressed();
    void spaceKeyPressed();
    void ChangeColor(GraphNode* start,GraphNode* end,QColor color);
public:
    Tab(QWidget* parent=nullptr);

};
class MainWindow : public QMainWindow
{
    Q_OBJECT
private:

    QTabWidget* tabWidget;

    QToolBar* tools=new QToolBar("Панель инструментов",this);

    QToolBar* graphSwitcher=new QToolBar("Панель графов",this);

    QAction* Manipulator=new QAction("Манипулятор",tools);

    QAction* EdgeAdder=new QAction("Создать ребро",tools);

    QAction* ArcAdder=new QAction("Создать дугу",tools);

    QAction* Deleter=new QAction("Удаление",tools);

    QAction* InfoAboutGraph=new QAction("Вывести информацию о графе",this);

    QAction* CreateNewGraph=new QAction("Создать новый граф",this);

private slots:

    void CurrentTool(QAction* action);

    void createNewGraph();

public:

    MainWindow(QWidget *parent = nullptr);

signals:

    void Info();

};

#endif // MAINWINDOW_H
