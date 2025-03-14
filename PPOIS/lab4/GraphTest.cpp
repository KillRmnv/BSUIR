#include <gtest/gtest.h>
#include "Graph.h"

TEST(GraphTest, AddVertex) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);

    EXPECT_TRUE(g.checkVertexExistance(1));
    EXPECT_TRUE(g.checkVertexExistance(2));
    EXPECT_EQ(g.vertexCount(), 2);
}

TEST(GraphTest, AddDuplicateVertex) {
    Graph<int> g;
    g.addVertex(1);
    EXPECT_THROW(g.addVertex(1), std::invalid_argument);
}

TEST(GraphTest, AddEdge) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addEdge(1, 2);

    EXPECT_TRUE(g.edgeExists({1, 2}));
    EXPECT_EQ(g.edgeCount(), 1);
    EXPECT_EQ(g.vertexDegree(1), 1);
    EXPECT_EQ(g.vertexDegree(2), 0);
}

TEST(GraphTest, AddDuplicateEdge) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addEdge(1, 2);
    EXPECT_NO_THROW(g.addEdge(1, 2)); // Дублирование разрешено в вашем коде
}

TEST(GraphTest, AddSelfLoop) {
    Graph<int> g;
    g.addVertex(1);
    EXPECT_THROW(g.addEdge(1, 1), std::invalid_argument);
}

TEST(GraphTest, RemoveEdge) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addEdge(1, 2);
    g.removeEdge({1, 2});

    EXPECT_FALSE(g.edgeExists({1, 2}));
    EXPECT_EQ(g.edgeCount(), 0);
}

TEST(GraphTest, RemoveNonexistentEdge) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    EXPECT_THROW(g.removeEdge({1, 2}), std::invalid_argument);
}

TEST(GraphTest, RemoveVertex) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addEdge(1, 2);
    g.removeVertex(1);

    EXPECT_FALSE(g.checkVertexExistance(1));
    EXPECT_TRUE(g.checkVertexExistance(2));
    EXPECT_EQ(g.vertexCount(), 1);
    EXPECT_EQ(g.edgeCount(), 0);
}

TEST(GraphTest, RemoveNonexistentVertex) {
    Graph<int> g;
    EXPECT_THROW(g.removeVertex(1), std::invalid_argument);
}

TEST(GraphTest, VertexDegree) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addVertex(3);
    g.addEdge(1, 2);
    g.addEdge(1, 3);

    EXPECT_EQ(g.vertexDegree(1), 2);
    EXPECT_EQ(g.vertexDegree(2), 0);
    EXPECT_EQ(g.vertexDegree(3), 0);
}

TEST(GraphTest, VertexDegreeNonexistent) {
    Graph<int> g;
    EXPECT_THROW(g.vertexDegree(1), std::invalid_argument);
}

TEST(GraphTest, EdgeIterator) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addVertex(3);
    g.addEdge(1, 2);
    g.addEdge(2, 3);

   auto it= EdgeIterator<int>(g.beginEdges());
    EXPECT_EQ(*it, std::make_pair(1, 2));
    ++it;
    EXPECT_EQ(*it, std::make_pair(2, 3));
}

TEST(GraphTest, ReverseEdgeIterator) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addVertex(3);
    g.addEdge(1, 2);
    g.addEdge(2, 3);

    auto it = g.rbeginEdges();
    EXPECT_EQ(*it, std::make_pair(2, 3));
    ++it;
    EXPECT_EQ(*it, std::make_pair(1, 2));
}

TEST(GraphTest, RemoveEdgeWithIterator) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addEdge(1, 2);

    auto it = g.beginEdges();
    g.removeEdge(it);

    EXPECT_EQ(g.edgeCount(), 0);
    EXPECT_FALSE(g.edgeExists({1, 2}));
}

TEST(GraphTest, RemoveVertexWithIterator) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addEdge(1, 2);

    IncedentVertexIterator it(1, g);
    g.removeVertex(it);

    EXPECT_TRUE(g.checkVertexExistance(1));
    EXPECT_FALSE(g.checkVertexExistance(2));
    EXPECT_EQ(g.vertexCount(), 1);
}

TEST(GraphTest, IncidentVertexIterator) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addVertex(3);
    g.addEdge(1, 2);
    g.addEdge(1, 3);

  IncedentVertexIterator it(1, g);
    EXPECT_EQ(*it, 2);
    ++it;
    EXPECT_EQ(*it, 3);
}

TEST(GraphTest, IncidentEdgeIterator) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addVertex(3);
    g.addEdge(1, 2);
    g.addEdge(1, 3);

    EdgeIncedentToVertexIterator it(1, g);
    EXPECT_EQ(*it, std::make_pair(1, 2));
    ++it;
    EXPECT_EQ(*it, std::make_pair(1, 3));
}

TEST(GraphTest, EdgeExists) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addEdge(1, 2);

    EXPECT_TRUE(g.edgeExists({1, 2}));
    EXPECT_FALSE(g.edgeExists({2, 3}));
}

TEST(GraphTest, CheckVertexExistance) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);

    EXPECT_TRUE(g.checkVertexExistance(1));
    EXPECT_TRUE(g.checkVertexExistance(2));
    EXPECT_FALSE(g.checkVertexExistance(3));
}

TEST(GraphTest, ClearGraph) {
    Graph<int> g;
    g.addVertex(1);
    g.addVertex(2);
    g.addEdge(1, 2);

    g.clear();

    EXPECT_TRUE(g.empty());
    EXPECT_EQ(g.vertexCount(), 0);
    EXPECT_EQ(g.edgeCount(), 0);
}


int main(int argc, char** argv) {
    setlocale(LC_ALL, "ru");
    std::locale::global(std::locale("ru_RU.UTF-8"));
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}