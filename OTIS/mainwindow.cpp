#include "mainwindow.h"
#include <QMessageBox>
#include<QBrush>

void Tab::showNextCycleNotification(QGraphicsScene* scene, std::vector<std::vector<unsigned int>>& cycles, int& currentIndex) {
    while (true) {

        if (currentIndex >= cycles.size()) {
            QMessageBox::information(this, "Результат", "Больше путей нет.");
            return;
        }
        for (int i = 0; i < Nodes.size(); ++i) {
            Nodes[i]->setId("");
        }
        if(currentIndex>0){
            int buff=currentIndex-1;
        for (int i = 0; i < cycles[buff].size()-1; ++i) {
            emit ChangeColor(Nodes[cycles[buff][i]],Nodes[cycles[buff][i+1]],Qt::black);
        }
        }
        const auto& cycle = cycles[currentIndex];
        for (int i = 0; i < cycle.size()-1; ++i) {
            QString buff = Nodes[cycle[i]]->getIdentificator();
            if(!buff.isEmpty())
            buff += ",";
            buff+=QString::number(i + 1);
            Nodes[cycle[i]]->setId(buff);
            emit ChangeColor(Nodes[cycle[i]],Nodes[cycle[i+1]],Qt::red);
        }
        QString buff = Nodes[cycle[cycle.size()-1]]->getIdentificator();
        if(!buff.isEmpty())
        buff += ",";
        buff+=QString::number(cycle.size());
        Nodes[cycle[cycle.size()-1]]->setId(buff);
        bool actionHandled = false;
        QEventLoop loop;

        connect(this, &Tab::EsckeyPressed, [&]() {
            if (!actionHandled) {
                actionHandled = true;
                currentIndex = cycles.size();
                for (int i = 0; i < cycle.size()-1; ++i) {
                    emit ChangeColor(Nodes[cycle[i]],Nodes[cycle[i+1]],Qt::black);
                }
                loop.quit();
            }
        });

        connect(this, &Tab::spaceKeyPressed, [&]() {
            if (!actionHandled) {
                actionHandled = true;
                currentIndex++;
                loop.quit();
            }
        });

        loop.exec();
    }
}

void Tab::keyPressEvent(QKeyEvent* event){
    if(event->key()==Qt::Key_Escape){
        emit EsckeyPressed();
    }else if(event->key()==Qt::Key_Space){
        emit spaceKeyPressed();
    }
}

void Tab::mousePressEvent(QMouseEvent *event){
    if(event->button()==Qt::RightButton){
        QMenu contextMenu;

               QAction* actionCycles = contextMenu.addAction("Эйлеровы циклы");
               QAction* actionTree = contextMenu.addAction("Дерево");
               QAction* actionBinTree=contextMenu.addAction("Бинарное дерево");

               QAction* selectedAction = contextMenu.exec(event->screenPos().toPoint());
                if(selectedAction==actionCycles){
                    EulerianCycle check;
                    std::vector<std::vector<unsigned int>> cycles=check.EulirianCycles(graph);
                    if(cycles.empty()){
                             QMessageBox::information(this, "Результат", "В этом графе нет циклов.");
                    }else{
                        std::vector<QString> identificators;
                        for(int i=0;i<Nodes.size();++i){
                            identificators.push_back(Nodes[i]->getIdentificator());
                        }
                        int currentIndex = 0;
                         showNextCycleNotification(scene, cycles, currentIndex);
                        for(int i=0;i<Nodes.size();++i){
                            Nodes[i]->setId(identificators[i]);
                        }
                    }
                }else if(selectedAction==actionTree){
                    Tree check;
                    for(int i=0;i<Nodes.size();i++){
                        emit Nodes[i]->deleteGraphicalRepresent(Nodes[i]);
                    }
                    std::vector<SubGraph> trees=check.Trees(graph);
                    graph.del();

                    int index=0;
                    for(int i=0;i<trees.size();++i){
                        trees[i].convert(index,graph);
                        index+=trees[i].size();
                    }
                    for(size_t  vert=0;vert<graph.getAdjList().size();vert++){
                        for(size_t i=0;i<graph.getAdjList()[vert].size();++i){
                            Arc* newArc=new Arc(Nodes[vert],Nodes[graph.getAdjList()[vert][i]],nullptr);
                            newArc->setStartPoint(Nodes[vert]);
                            newArc->setEndPoint(Nodes[graph.getAdjList()[vert][i]]);
                            scene->addItem(newArc);
                            QRectF sceneRect = scene->sceneRect();
                            connect(newArc,&Arc::delet,this,&Tab::deleteArc);
                            if (!sceneRect.contains(newArc->sceneBoundingRect())) {
                                scene->setSceneRect(sceneRect.united(newArc->sceneBoundingRect()));
                            }
                        }
                    }
                }else if(selectedAction==actionBinTree){
                    BinTree check;
                    for(int i=0;i<Nodes.size();i++){
                        emit Nodes[i]->deleteGraphicalRepresent(Nodes[i]);
                    }
                    std::vector<SubGraph> trees=check.Trees(graph);
                    graph.del();

                    int index=0;
                    for(int i=0;i<trees.size();++i){
                        trees[i].convert(index,graph);
                        index+=trees[i].size();
                    }
                    for(size_t  vert=0;vert<graph.getAdjList().size();vert++){
                        for(size_t i=0;i<graph.getAdjList()[vert].size();++i){
                            Arc* newArc=new Arc(Nodes[vert],Nodes[graph.getAdjList()[vert][i]],nullptr);
                            newArc->setStartPoint(Nodes[vert]);
                            newArc->setEndPoint(Nodes[graph.getAdjList()[vert][i]]);
                            scene->addItem(newArc);
                            QRectF sceneRect = scene->sceneRect();
                            connect(newArc,&Arc::delet,this,&Tab::deleteArc);
                            if (!sceneRect.contains(newArc->sceneBoundingRect())) {
                                scene->setSceneRect(sceneRect.united(newArc->sceneBoundingRect()));
                            }
                        }
                    }
                }
            }
        }

void Tab::InfoAboutgraph() {
    QDialog *dialog = new QDialog(this);
    QVBoxLayout *layout = new QVBoxLayout(dialog);
    QTextEdit *textEdit = new QTextEdit(dialog);
    QString info="Вершин:";
    info+=QString::number(graph.getVertexCount(),10);
    info+=" Ребер:";
    info+=QString::number(graph.getEdgeCount(),10);
    info+="\n";
    EulerianCycle check;
    if(!check.isEulerian(graph)){
        info+="Граф имеет эйлеров цикл\n";
    }else{
        info+="Граф не имеет эйлеров цикл\n";
    }
    textEdit->setPlainText(info);
    textEdit->setReadOnly(true);
    layout->addWidget(textEdit);
    dialog->setLayout(layout);
    dialog->resize(500, 300);
    dialog->exec();
}

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent),
      tabWidget(new QTabWidget(this)),
      tools(new QToolBar("Инструменты", this)),
      graphSwitcher(new QToolBar("Переключение графов", this))
{
    setCentralWidget(tabWidget);
    addToolBar(Qt::TopToolBarArea, tools);
    setFixedSize(1920, 1080);
    tools->setFixedWidth(1920);
    tools->setFixedHeight(60);
    tools->addAction(Manipulator);
    tools->addAction(EdgeAdder);
    tools->addAction(ArcAdder);
    tools->addAction(Deleter);
    tools->addAction(InfoAboutGraph);
    tools->addAction(CreateNewGraph);
    connect(tools, &QToolBar::actionTriggered, this, &MainWindow::CurrentTool);

    TOOL.setCurrentTool(Tool::Manipulator);
}

Tab::Tab(QWidget* parent) : QTabWidget(parent) {
    scene = new QGraphicsScene(this);
    view = new QGraphicsView(scene, this);
    scene->setSceneRect(-10000, -10000, 20000, 20000);
    view->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    view->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    view->setRenderHint(QPainter::Antialiasing);
    view->setRenderHint(QPainter::Antialiasing);
    currentNode=nullptr;

    QVBoxLayout *layout = new QVBoxLayout(this);
    layout->addWidget(view);
    setLayout(layout);
}

void Tab::setCurrentNode(GraphNode* node){
    if(currentNode!=nullptr&&node!=currentNode){
        currentNode->setNodeColor(currentNode->getColor());
    }
    currentNode=node;
}

void Tab::inputDialog(GraphNode* node){
        QString graphName = QInputDialog::getText(this, tr("Идентификатор"), tr("Введите идентификатор:"));
        node->setId(graphName);

}

void Tab::changeColor(GraphNode* node){
const QColor selectedColor = QColorDialog::getColor(Qt::white, this, "Select Color");
if(selectedColor!=Qt::red){
    node->setNodeColor(selectedColor);
}
}

void Tab::nodeDelete(GraphNode * node){
    currentNode=nullptr;
    int buff=0;
    for(int i=0;i<Nodes.size();++i){
        if(Nodes[i]==node){
            graph.delNode(node->getID());
            Nodes.erase(Nodes.begin()+i);
            buff=i;
            break;
        }
    }
    for(int i=buff+1;i<Nodes.size();++i){
        Nodes[i]->decreaseIDByOne();
    }
    graph.DecreaseVertexCountByOne();
}
void Tab::shortest(int end){
    ShortestPath path;
    int Path=path.shortestDistanceBFS(graph,currentNode->getID(),end);
    QMessageBox Info;
    QMessageBox::information(this, "Результат", QString::number(Path,10));
}

void Tab::findPaths(int end){
    AllPaths pathsGenerator;
    std::vector<std::vector<unsigned int>> paths=pathsGenerator.GeneratePaths(graph,currentNode->getID(),end);
    std::vector<QString> identificators;
    for(int i=0;i<Nodes.size();++i){
        identificators.push_back(Nodes[i]->getIdentificator());
    }
    int currentIndex = 0;
     showNextCycleNotification(scene, paths, currentIndex);
    for(int i=0;i<Nodes.size()-1;++i){
        Nodes[i]->setId(identificators[i]);
    }
     Nodes[Nodes.size()-1]->setId(identificators[Nodes.size()-1]);
     for(auto& path:paths){
         for(int i=0;i<path.size()-1;++i){
             emit ChangeColor(Nodes[path[i]],Nodes[path[i+1]],Qt::black);
         }
     }
}

void Tab::CreateNode(QPointF xy) {

    GraphNode* newNode = new GraphNode("Node 1",nullptr,graph.getAdjList().size(),xy);
    graph.push_back(std::vector<unsigned int>());
    newNode->setRect(xy.x()-10,xy.y()-10, 2 * 10, 2 * 10);
    scene->addItem(newNode);
    Nodes.push_back(newNode);
    connect(newNode, &GraphNode::nodeClicked, this, &Tab::setCurrentNode);
    connect(newNode,&GraphNode::changeIdentificator,this,&Tab::inputDialog);
    connect(newNode,&GraphNode::Color,this,&Tab::changeColor);
    connect(newNode,&GraphNode::Arc,this,&Tab::CreateArc);
    connect(newNode,&GraphNode::Edge,this,&Tab::CreateEdge);
    connect(newNode,&GraphNode::deleteINGraph,this,&Tab::nodeDelete);
    connect(newNode,&GraphNode::paths,this,&Tab::findPaths);
    connect(newNode,&GraphNode::shortestPath,this,&Tab::shortest);


    QRectF sceneRect = scene->sceneRect();
    if (!sceneRect.contains(newNode->sceneBoundingRect())) {
           scene->setSceneRect(sceneRect.united(newNode->sceneBoundingRect()));
       }
}

void Tab::deleteArc(int start,int end){
    auto It=std::find(graph.getAdjList()[start].begin(),graph.getAdjList()[start].end(),end);
    graph.getAdjList()[start].erase(It);
    graph.decreaseEdgeCountByOne();
}

void Tab::deleteEdge(int start,int end){
    auto It=std::find(graph.getAdjList()[start].begin(),graph.getAdjList()[start].end(),end);
    graph.getAdjList()[start].erase(It);
    It=std::find(graph.getAdjList()[end].begin(),graph.getAdjList()[end].end(),start);
    graph.getAdjList()[end].erase(It);
    graph.decreaseEdgeCountByOne();
}

void Tab::CreateArc(GraphNode* node) {
    if (!currentNode) return;
    Arc* newArc = new Arc(currentNode,node,nullptr);
    graph.push_backArc(currentNode->getID(),node->getID());
    newArc->setStartPoint(currentNode);
    newArc->setEndPoint(node);
    scene->addItem(newArc);
    QRectF sceneRect = scene->sceneRect();
    connect(newArc,&Arc::delet,this,&Tab::deleteArc);
    connect(this,&Tab::ChangeColor,newArc,&Arc::changeColor);
    if (!sceneRect.contains(newArc->sceneBoundingRect())) {
        scene->setSceneRect(sceneRect.united(newArc->sceneBoundingRect()));
    }
}

void Tab::CreateEdge(GraphNode* node) {
    if (!currentNode) return;

    Edge* newArc = new Edge(currentNode,node,nullptr);
    graph.push_backEdge(currentNode->getID(),node->getID());
    newArc->setStartPoint(currentNode);
    newArc->setEndPoint(node);
    scene->addItem(newArc);
    connect(newArc,&Arc::delet,this,&Tab::deleteEdge);
    connect(this,&Tab::ChangeColor,newArc,&Arc::changeColor);

    QRectF sceneRect = scene->sceneRect();
    if (!sceneRect.contains(newArc->sceneBoundingRect())) {
        scene->setSceneRect(sceneRect.united(newArc->sceneBoundingRect()));
    }
}

void Tab::mouseDoubleClickEvent(QMouseEvent *event) {
    if (event->button() == Qt::LeftButton&& TOOL.getCurrentTool()==Tool::Manipulator) {
        QPointF scenePos = view->mapToScene(view->mapFromParent(event->pos()));
          CreateNode(scenePos);
    }
}

void MainWindow::createNewGraph() {
    QString graphName = QInputDialog::getText(this, tr("Создание графа"), tr("Введите название"));
    if (!graphName.isEmpty()) {
        Tab* newT=new Tab();
        connect(this,&MainWindow::Info,newT,&Tab::InfoAboutgraph);
        tabWidget->addTab(newT, graphName);
        tabWidget->setCurrentWidget(newT);
    }
}

void MainWindow::CurrentTool(QAction* action) {
    if (action == Manipulator) {
        TOOL.setCurrentTool(Tool::Manipulator);
    } else if (action == EdgeAdder) {
        TOOL.setCurrentTool(Tool::EdgeCreator);
    }else if(action==InfoAboutGraph){
       emit Info();
    } else if (action == CreateNewGraph) {
        createNewGraph();
    }else if(action==ArcAdder){
        TOOL.setCurrentTool(Tool::ArcCreator);
    }else if(action==Deleter){
        TOOL.setCurrentTool(Tool::Delete);
    }
}
