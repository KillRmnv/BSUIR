classDiagram
direction BT
class Доставка {
   varchar(64) Тип
   date Дата
   integer delivery_id
}
class Издания {
   varchar(64) Название
   integer Периодичность  выхода
   varchar(64) Тип
   integer Индекс
}
class История выдачи {
   date Дата
   integer employee_id
   integer Издание
   integer Номер издания
   integer Выписан
   integer Получен
}
class Подписки {
   integer Индекс издания
   integer employee_id
   date Дата начала
   date Дата окончания
   integer Доставка
   integer Период
   integer Стоимость
}
class Сотрудники {
   varchar(64) Фамилия
   varchar(64) Имя
   varchar(64) Отчество
   varchar(64) Должность
   varchar(64) Подразделение
   integer employee_id
}

История выдачи  -->  Издания : Издание:Индекс
История выдачи  -->  Сотрудники : employee_id
Подписки  -->  Доставка : Доставка:delivery_id
Подписки  -->  Издания : Индекс издания:Индекс
Подписки  -->  Сотрудники : employee_id
