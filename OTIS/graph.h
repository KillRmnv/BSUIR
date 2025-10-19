#pragma once
#include <algorithm>
#include<vector>
#include <iostream>
#include<unordered_map>
#include<stack>
#include<queue>
#include <unordered_set>

class Graph {
protected:
    std::vector<std::vector<unsigned int> > adjList;
    int V = 0;
    int E = 0;
public:
   virtual void pop_back() {
    adjList.pop_back();
    }
    void sort() {
        for (auto &neighbors : adjList) {
            std::sort(neighbors.begin(), neighbors.end());
        }
    }
    std::vector<std::vector<unsigned int> >& getAdjList() { return adjList; }
    void push_back(std::vector<unsigned int> neighbors) {
        adjList.push_back(neighbors);
        V++;
    }
    int size() { return V; }
    std::vector<unsigned int> &operator[](unsigned int index) {
        return adjList[index];
    }
    const std::vector<unsigned int> &operator[](unsigned int index) const {
        return adjList[index];
    }
    void push_backEdge(unsigned int vertex, unsigned int neighbor) {
        while (vertex >= adjList.size()) {
            adjList.push_back(std::vector<unsigned int>());
            V++;
        }

        while (neighbor >= adjList.size()) {
            adjList.push_back(std::vector<unsigned int>());
            V++;
        }
        adjList[vertex].push_back(neighbor);
        adjList[neighbor].push_back(vertex);
        E++;
    }
    void push_backArc(unsigned int vertex, unsigned int neighbor) {
        while (vertex >= adjList.size()) {
            adjList.push_back(std::vector<unsigned int>());
            V++;
        }

        while (neighbor >= adjList.size()) {
            adjList.push_back(std::vector<unsigned int>());
            V++;
        }
        adjList[vertex].push_back(neighbor);
        E++;
    }
    int getVertexCount() { return V; }
    int getEdgeCount() { return E; }
    void DecreaseEdgeCountByOne() { E--; }
    void DecreaseVertexCountByOne() { V--; }
    bool isEmpty() { return adjList.empty(); }
    bool checkForSufficientCondition(int &edges, int &vertexes) {
        return edges > 3 * vertexes - 3;
    }
    void increaseVertexCount() { V++; }
    virtual void print() {
       std::cout << std::endl;
        for (int i = 0; i < adjList.size(); i++) {
            std::cout << i << ":";
            for (auto vertex: adjList[i]) {
                std::cout << vertex << " ";
            }
            std::cout << std::endl;
        }
    }
    void decreaseEdgeCountByOne() { E--; }
    void delNode(int index) {
        for (auto &vertex : adjList) {
            vertex.erase(std::remove(vertex.begin(), vertex.end(), index), vertex.end());
            for (auto &v : vertex) {
                if (v > index) {
                    --v;
                }
            }
        }
        adjList.erase(adjList.begin() + index);
        --V;
    }

   void del(){
        for(auto vertex:adjList){
            vertex.clear();
        }
        adjList.clear();
        V=0;E=0;
    }
};
class SubGraph:public Graph {
private:
    std::unordered_map<unsigned int, unsigned int> vertexMap;
public:
    void convert(int index,Graph& graph){
        for(int i=0;i<adjList.size();++i){
            vertexMap[i]=vertexMap[i]+index;
        }
        for(int i=0;i<adjList.size();++i){
            for(int j=0;j<adjList[i].size();++j){
                graph.push_backArc(vertexMap[i],vertexMap[adjList[i][j]]);
            }
        }
    }
    void print() override {
        std::cout << std::endl;
        for (int i = 0; i < adjList.size(); i++) {
            std::cout << i << ":";
            for (auto vertex: adjList[i]) {
                std::cout << vertex << "("<<vertexMap[vertex]<<") ";
            }
            std::cout << std::endl;
        }
    }
    void setVertexMap( std::unordered_map<unsigned int, unsigned int>& map) {
        vertexMap = map;
    }
    void pop_back() override{
        int buff=adjList.size()-1;
        adjList.pop_back();
        auto it=std::find(adjList[adjList.size() - 1].begin(),adjList[adjList.size() - 1].end(),buff);
        if (adjList.size()>0)
        adjList[adjList.size() - 1].erase(it);
    }
   void convertIn(unsigned int realNum,unsigned int numInAdjList ) {
       vertexMap[realNum] = numInAdjList;
   }
    unsigned int convertOut(unsigned int realNum) {
       return vertexMap[realNum];
   }
    std::unordered_map<unsigned int, unsigned int>& getVertexMap() { return vertexMap; }
    void clear() {
       for (auto &neighbors : adjList) {
           neighbors.clear();
       }
        V=0;E=0;
   }
};
class StronglyConnectedComponents {
public:
   static   std::vector<SubGraph>  getStronglyConnectedComponents(Graph &graph) {
       graph.sort();
        int V = graph.getVertexCount();
        std::vector<SubGraph> scc;
        if (V == 0) return scc;

        std::vector<bool> visited(V, false);
        std::stack<int> finishStack;
        for (int i = 0; i < V; ++i) {
            if (!visited[i]) {
                dfs(graph, i, visited, finishStack);
            }
        }

        Graph transposedGraph = transpose(graph);
        std::fill(visited.begin(), visited.end(), false);
        while (!finishStack.empty()) {
            int v = finishStack.top();
            finishStack.pop();

            if (!visited[v]) {
                SubGraph component;
                collectComponent(transposedGraph, v, visited, component);
                scc.push_back(component);
            }
        }
        return scc;
    }
private:
    static void dfs(Graph &graph, int v, std::vector<bool> &visited, std::stack<int> &finishStack) {
        visited[v] = true;
        for (unsigned int neighbor : graph[v]) {
            if (!visited[neighbor]) {
                dfs(graph, neighbor, visited, finishStack);
            }
        }
        finishStack.push(v);
    }

    static void collectComponent(Graph &graph,unsigned int v, std::vector<bool> &visited, SubGraph &component) {
        visited[v] = true;
        if (component.getVertexMap().find(v)==component.getVertexMap().end()) {
            component.convertIn( v,component.getVertexCount());
            component.push_back(std::vector<unsigned int>());
        }
        for (size_t i = 0; i < graph.getAdjList()[v].size(); i++) {
            if (!visited[graph.getAdjList()[v][i]]) {
                if (component.getVertexMap().find(graph.getAdjList()[v][i])==component.getVertexMap().end()) {
                    component.convertIn( graph.getAdjList()[v][i],component.getVertexCount());
                }
                if (std::find(graph.getAdjList()[graph.getAdjList()[v][i]].begin(),
                    graph.getAdjList()[graph.getAdjList()[v][i]].end(),v) != graph.getAdjList()[graph.getAdjList()[v][i]].end()) {
                    component.push_backEdge(component.convertOut(v), component.convertOut(graph.getAdjList()[v][i]));
                }
                else {
                    component.push_backArc(component.convertOut(v),component.convertOut(graph.getAdjList()[v][i]));
                }
                collectComponent(graph, graph.getAdjList()[v][i], visited, component);
            }else {
                if (std::find(graph.getAdjList()[graph.getAdjList()[v][i]].begin(),
                    graph.getAdjList()[graph.getAdjList()[v][i]].end(),v) == graph.getAdjList()[graph.getAdjList()[v][i]].end()
                    &&component.convertOut(graph.getAdjList()[v][i])==0) {
                    component.push_backArc(component.convertOut(v), component.convertOut(graph.getAdjList()[v][i]));
                    }
            }
        }
    }

    static Graph transpose(Graph &graph) {
        Graph transposedGraph;
        //graph.print();
        for (int v = 0; v < graph.getVertexCount(); ++v) {
            for (auto neighbor : graph[v]) {
                transposedGraph.push_backArc(neighbor, v);
            }
            if (graph[v].empty()) {
                transposedGraph.push_back(std::vector<unsigned int>());
            }

        }

        return transposedGraph;
    }
};

class EulerianCycle {
protected:


    virtual void add() {

            allPaths.push_back(currentPath);
    }
    struct pair_hash {
        template <typename T1, typename T2>
        std::size_t operator()(const std::pair<T1, T2>& p) const {
            std::size_t h1 = std::hash<T1>{}(p.first);
            std::size_t h2 = std::hash<T2>{}(p.second);
            return h1 ^ (h2 << 1);
        }
    };
    struct Edge {
        int from, to;
        bool used;
        Edge() : from(-1), to(-1), used(false) {}
        Edge(int f, int t) : from(f), to(t), used(false) {}
    };
    std::unordered_map<std::pair<unsigned int,unsigned int >,Edge,pair_hash> edges;
    std::vector<unsigned int> currentPath;
    std::vector<std::vector<unsigned int>> allPaths;
     virtual bool check(int v, int start, int& edgeCount, int &usedEdges) {
        return usedEdges == edgeCount &&v==start;
    }
     void dfs(int v, int start, int edgeCount, int &usedEdges,Graph & graph,int & convert) {
        if (check(v,start,edgeCount,usedEdges)) {
            add();
            return;
        }
        for (int i = 0; i < graph.getAdjList()[v].size(); ++i) {
            if (graph.getAdjList()[v][i] !=currentPath[currentPath.size()-1]) {
                if (edges.find({v,graph.getAdjList()[v][i]}) == edges.end()&&edges.find({graph.getAdjList()[v][i],v}) == edges.end()) {
                    edges[{v,graph.getAdjList()[v][i]}]=Edge(v,graph.getAdjList()[v][i]);
                    edges[{graph.getAdjList()[v][i],v}]=Edge(graph.getAdjList()[v][i],v);
                }
                Edge &e=edges[{v,graph.getAdjList()[v][i]}];
                Edge &e1=edges[{graph.getAdjList()[v][i],v}];
                if (!e.used) {
                    e1.used=true;
                    e.used = true;
                    ++usedEdges;

                    currentPath.push_back(e.to);
                    dfs(e.to, start, edgeCount, usedEdges,graph,convert);

                    e.used = false;
                    e1.used = false;
                    --usedEdges;
                    if (currentPath.size()>0)
                        currentPath.pop_back();
                }
            }
        }
    }
    virtual int Point(int start,int end ) {
         return start;
     }
     virtual int begin(){
         return 0;
     }
     virtual  bool condition(int start,Graph& graph){
        return start < graph.getAdjList().size();
     }
     void pathFinding(Graph &graph,int end) {
        int edgeCount = graph.getEdgeCount();
        int usedEdges = 0,convert=0,point;
            for (int start = begin(); condition(start,graph); ++start) {
                point = Point(start,end);
                convert=0;
                if (!graph.getAdjList()[start].empty()) {
                    //edges.clear();
                    currentPath.clear();
                    currentPath.push_back(start);
                    dfs(start, point, edgeCount, usedEdges,graph,convert);
                }
            }
    }
    public:
    EulerianCycle()=default;
     bool isEulerian(Graph &graph) {
        auto components = StronglyConnectedComponents::getStronglyConnectedComponents(graph);
        if (components.size() == 1) {
            pathFinding(graph,0);
        }
        return allPaths.empty();
    }
    std::vector<std::vector<unsigned int>>& EulirianCycles(Graph &graph) {
        auto components = StronglyConnectedComponents::getStronglyConnectedComponents(graph);
        if (components.size() == 1) {
            pathFinding(graph,0);
        }

            return allPaths;
    }
};
class Tree {
public:
    std::vector<SubGraph> Trees(Graph &graph) {
        auto components = StronglyConnectedComponents::getStronglyConnectedComponents(graph);
        std::vector<SubGraph> trees;

        for (auto &component : components) {
            SubGraph current;
            current.setVertexMap(component.getVertexMap());
            std::vector<bool> visited(component.size(), false);

            #pragma omp parallel for
            for (unsigned int start = 0; start < component.size(); ++start) {
                if (!visited[start]) {
                    DFS(component, start, visited, current);
                }
            }
            #pragma omp critical
            trees.push_back(current);
        }

        return trees;
    }

    virtual bool childsCheck( unsigned int& v) {
        return true;
    }

private:
    void DFS( SubGraph &component, unsigned int currentVertex,
             std::vector<bool> &visited, SubGraph &tree) {
        visited[currentVertex] = true;

        for (size_t neighbor=0 ; neighbor<component.getAdjList()[currentVertex].size();++neighbor) {
            if (!visited[component.getAdjList()[currentVertex][neighbor]] && childsCheck( currentVertex)) {
                tree.push_backArc(currentVertex, component.getAdjList()[currentVertex][neighbor]);
                DFS(component, component.getAdjList()[currentVertex][neighbor], visited, tree);
            }
        }
    }
};
class BinTree : public Tree {
private:
    std::unordered_map<unsigned int,unsigned int> map;
public:
    bool childsCheck(unsigned int& v) override {
        if(map.find(v)==map.end()){
            map[v]=1;
            return true;
        }

        unsigned int buff=map[v];
        if(buff<2){
            buff++;
            map[v]=buff;
            return true;
        }
        return false;

    }
};

class ShortestPath {
public:
    int shortestDistanceBFS(Graph &graph, int start, int end) {
        std::queue<int> q;
        std::vector<int> distance(graph.getVertexCount(), -1);

        q.push(start);
        distance[start] = 0;

        while (!q.empty()) {
            int current = q.front();
            q.pop();

            for (int neighbor : graph[current]) {
                if (distance[neighbor] == -1) {
                    distance[neighbor] = distance[current] + 1;
                    q.push(neighbor);

                    if (neighbor == end) {
                        return distance[neighbor];
                    }
                }
            }
        }

        return -1;
    }

};
class AllPaths : public EulerianCycle{
private:
    unsigned int Start;
    void add() override{
        allPaths.push_back(currentPath);
    }
    int Point(int start,int end) override {
        return end;
    }
     bool check(int v, int start, int& edgeCount, int &usedEdges) override{
        return v==start;
    }
     bool condition(int start,Graph& graph) override {
             return Start==start;
          }
     int begin() override{
              return Start;
          }
public:
    AllPaths()=default;
    std::vector<std::vector<unsigned int>>& GeneratePaths(Graph &graph,unsigned int strt,unsigned int end) {
        Start=strt;
        pathFinding(graph,end);
        return allPaths;
    }
};
