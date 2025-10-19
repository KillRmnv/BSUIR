#ifndef TOOL_H
#define TOOL_H


#include <QObject>

class Tool : public QObject {
    Q_OBJECT
public:
    enum ToolType {
        Manipulator,
        ArcCreator,
        EdgeCreator,
        Delete,
    };

    explicit Tool(QObject* parent = nullptr)
        : QObject(parent), currentTool(Manipulator) {}

    ToolType getCurrentTool() const { return currentTool; }
    void setCurrentTool(ToolType tool) { currentTool = tool; }

signals:
    void toolChanged(ToolType newTool);

private:
    ToolType currentTool;
};
extern Tool TOOL;

#endif // TOOL_H
