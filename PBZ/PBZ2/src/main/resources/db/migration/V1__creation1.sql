

create table if not exists public."Издания"(
"Название" varchar(64),
"Индекс" integer primary key 
check("Индекс">0),
"Периодичность  выхода" integer, 
constraint chk_period check ("Периодичность  выхода" > 0),
"Тип" varchar(64)
);


create table if not exists public."Сотрудники"(
employee_id serial PRIMARY KEY,
"Фамилия" varchar(64),
"Имя" varchar(64),
"Отчество" varchar(64),
"Должность" varchar(64),
"Подразделение" varchar(64)
);



create table if not exists public."Доставка"(
delivery_id serial primary key,
"Тип" varchar(64),
"Дата" DATE
);



create table if not exists public."Подписки"(
"Индекс издания" integer references "Издания"("Индекс"),
employee_id serial references "Сотрудники"(employee_id)
on delete cascade,
"Дата начала" DATE,
"Дата окончания" DATE,
"Доставка" integer references "Доставка"(delivery_id)
on delete cascade,
"Период" integer check( "Период">0),
"Стоимость" integer check ("Стоимость">0)
);
-- primary key


create table if not exists public."История выдачи"(
"Дата" DATE,
employee_id integer references "Сотрудники"(employee_id)
on delete cascade,
"Издание" integer references "Издания"("Индекс")
on delete cascade,
"Номер издания" integer ,
constraint chck_num_of_printing check( "Номер издания">0),
"Выписан" integer check ("Выписан"=0 or "Выписан"=1),
"Получен" integer check ("Получен"=0 or "Получен"=1)

);

--
--
-- drop table if exists "История выдачи";
-- drop table if exists "Подписки";
-- drop table if exists "Доставка";
-- drop table if exists "Сотрудники";
-- drop table if exists "Издания";