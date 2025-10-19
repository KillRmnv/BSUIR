#include "graphicobject.h"

GraphicObject::GraphicObject(QObject* parent)
    :  label(nullptr) {  // Не создаем метку здесь
    setLabelVisible(false);  // По умолчанию скрываем метку
}

GraphicObject::~GraphicObject() {
    delete label; // Освобождаем память для метки, если она была создана
}


