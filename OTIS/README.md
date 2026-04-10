# OTIS - Graph Theory Visualization Tool

OTIS is a Qt-based application for creating, manipulating, and analyzing graphs. The tool provides interactive visualization of graph theory concepts and algorithms.

## Features

- **Interactive Graph Creation**: Add nodes via double-click, create edges and arcs using toolbar tools
- **Graph Algorithms**:
  - Eulerian cycle detection and visualization
  - Tree and binary tree identification
  - Shortest path finding (BFS algorithm)
  - All paths enumeration between nodes
- **Visual Feedback**:
  - Path highlighting with animated color changes
  - Node labeling and identification
  - Interactive manipulation of graph elements
- **Multi-graph Support**: Tabbed interface for working with multiple graphs simultaneously
- **Context-sensitive Operations**: Right-click menu for algorithm selection

## Project Structure

- `main.cpp` - Application entry point
- `mainwindow.h/cpp` - Main window implementation with toolbar and tab management
- `graph.h` - Graph data structure and algorithm implementations
- `graphnode.h` - Visual graph node component (QGraphicsEllipseItem)
- `TOOL.h` - Global tool state manager

## Usage

1. **Creating Nodes**: Select the "Manipulator" tool and double-click on the canvas
2. **Creating Edges/Arcs**: 
   - Select a node (it will be highlighted)
   - Choose "Create Edge" or "Create Arc" from the toolbar
   - Click on another node to create the connection
3. **Running Algorithms**:
   - Right-click on any node to open the context menu
   - Select from: Eulerian cycles, Tree, or Binary tree
   - Results will be visualized on the graph
4. **Path Finding**:
   - Select a start node
   - Right-click and choose an algorithm
   - For shortest path/all paths, specify the end node when prompted
5. **Manipulating Elements**:
   - Drag nodes to reposition them
   - Right-click on nodes/edges to delete them
   - Use the "Deleter" tool for removal operations

## Technical Details

- Built with Qt framework using Graphics View architecture
- Custom Graph class with adjacency list representation
- Algorithm implementations based on DFS/BFS and strongly connected components
- Signal-slot mechanism for inter-component communication
- Tabbed interface for multiple graph instances

## Requirements

- Qt 5.x or later
- C++ compiler with C++11 support

## Building

The project includes a Qt project file (`test.pro`). To build:

```bash
qmake test.pro
make
```

## Notes

This is an educational project focused on graph theory visualization. The implementation prioritizes clarity of algorithm demonstration over production-level optimization.
