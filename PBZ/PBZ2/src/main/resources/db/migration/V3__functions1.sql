

drop function if exists find_printings_by_state(varchar);
-- Функция проверки состояния(получено или выдано)
create function find_printings_by_state(state_per varchar(64))
returns table (
    employee_id integer,
    "Издание" integer,
    "Номер издания" integer,
    "Выписан" integer,
    "Получен" integer
)
language sql
as $$
    select employee_id, "Издание", "Номер издания", "Выписан", "Получен"
    from "История выдачи"
    where 
        (state_per = 'Выписано' and "Выписан" = 1)
        or (state_per = 'Получено' and "Выписан" = 1 and "Получен" = 1)
        or (state_per not in ('Выписано', 'Получено'));
$$;


-- Функция для выведения сведений о выписанных и полученных номерах различных журналов и  газет. 
-- Принимает два параметра-состояние(получено или выдано) и тип(газета, или журнал, или все сразу)
drop function if exists find_printings_by_state_and_type(varchar,varchar);
create or replace function find_printings_by_state_and_type(
state_per varchar(64),
type_per varchar(64)
)
returns table (
	employee_id integer,
	"Издание" integer,
    "Номер издания" integer,
    "Выписан" integer,
    "Получен" integer,
	"Название" varchar(64),
	"Тип" varchar(64)
) language sql
as $$
select t2.employee_id,t2."Издание",t2."Номер издания",t2."Выписан",t2."Получен",t1."Название",t1."Тип" from
    find_printings_by_state(state_per) t2 join "Издания" t1
	on t1."Индекс"=t2."Издание"
    where 
        (type_per =  t1."Тип")
        or (type_per = 'Все');
$$;



-- Функция чтения из таблицы сотрудников
create or replace function read_subscription(    
	index_printing integer,
    emp_id integer,
    starting_date date,
    ending_date date,
    delivery integer,
    period_time integer,
	cost_var integer
) returns table(
"Индекс издания" integer ,
employee_id integer,
"Дата начала" DATE,
"Дата окончания" DATE,
"Доставка" integer,
"Период" integer,
"Стоимость" integer
) language sql
as $$
	select "Индекс издания"  ,employee_id ,"Дата начала" ,"Дата окончания" ,"Доставка" ,"Период" ,"Стоимость"  
	from "Подписки" where (index_printing < 0 or index_printing = "Индекс издания")
          and (emp_id < 0 or emp_id = employee_id)
          and (starting_date is null or "Дата начала" = starting_date)
          and (ending_date is null or "Дата окончания" = ending_date)
          and (delivery < 0 or "Доставка" = delivery)
          and (period_time < 0 or period_time = "Период")
		  and (cost_var<0 or cost_var="Стоимость");
$$;


-- Процедура обновления записи в таблице с подписками
create  or replace procedure update_subscription(
index_printing integer,
emp_id integer,
starting_date DATE,
ending_date DATE,
delivery integer,
period_time integer,
cost_var integer
) language sql
as $$ 
	update "Подписки" set "Индекс издания" = COALESCE(index_printing, "Индекс издания"),
    "Дата начала" = COALESCE(starting_date, "Дата начала"),
    "Дата окончания" = COALESCE(ending_date, "Дата окончания"),
    "Доставка" = COALESCE(delivery, "Доставка"),
    "Период" = COALESCE(period_time, "Период"),
	"Стоимость"=COALESCE(cost_var,"Стоимость")
	where employee_id=emp_id;
$$;

-- Процедура вставки записи в таблице с подписками
create or replace procedure insert_subsription(
index_printing integer,
emp_id integer,
starting_date DATE,
ending_date DATE,
delivery integer,
period_time integer,
cost_var integer
) language sql
as $$
	insert into "Подписки"("Индекс издания",employee_id,"Дата начала","Дата окончания","Доставка","Период","Стоимость") values
	(index_printing,emp_id,starting_date,ending_date,delivery,period_time,cost_var);
$$;
-- Функция удаления записи в таблице с подписками
drop function if exists delete_subscription(
     integer,
     integer,
     date,
     date,
     integer,
     integer,
	 integer);
create or replace function delete_subscription(
    index_printing integer,
    emp_id integer,
    starting_date date,
    ending_date date,
    delivery integer,
    period_time integer,
	cost_var integer
) 
returns integer
language sql
as $$
    with deleted as (
        delete from "Подписки"
        where (index_printing < 0 or index_printing = "Индекс издания")
          and (emp_id < 0 or emp_id = employee_id)
          and (starting_date is null or "Дата начала" = starting_date)
          and (ending_date is null or "Дата окончания" = ending_date)
          and (delivery < 0 or "Доставка" = delivery)
          and (period_time < 0 or period_time = "Период")
		  and (cost_var<0 or cost_var="Стоимость")
        returning 1
    )
    select count(*) from deleted;
$$;



-- Функция чтения из таблицы истории выдачи
create or replace function read_history( 
	date_var date,
	emp_id integer,
	publication_var integer,
	num_of_publication integer,
	write_out integer,
	recieved integer
) returns table(
"Дата" DATE,
employee_id integer,
"Издание" integer,
"Номер издания" integer ,
"Выписан" integer,
"Получен" integer
) language sql
as $$
	select "Дата",employee_id,"Издание","Номер издания" ,"Выписан","Получен" 
	from "История выдачи" where  (publication_var<0 or publication_var="Издание") and
	(emp_id<0 or emp_id=employee_id) and
	("Номер издания"=num_of_publication or num_of_publication<0) and
	(write_out="Выписан" or write_out<0) and
	("Получен"=recieved or recieved<0) and
	(date_var is null or date_var="Дата");
$$;


-- Процедура обновления записи в таблице с историей получения изданий
create or replace procedure update_history(
date_var date,
emp_id integer,
publication_var integer,
num_of_publication integer,
write_out integer,
recieved integer 
) language sql
as $$
 
	update "История выдачи" set "Издание" = COALESCE(publication_var, "Издание"),
    "Номер издания" = COALESCE(num_of_publication, "Номер издания"),
    "Выписан" = COALESCE(write_out, "Выписан"),
    "Получен" = COALESCE(recieved, "Получен"),
	"Дата"=COALESCE(date_var,"Дата")
	where employee_id=emp_id;

$$;

-- Процедура добавления записи в таблице с историей получения изданий
create or replace procedure insert_history(
date_var date,
emp_id integer,
publication_var integer,
num_of_publication integer,
write_out integer,
recieved integer 
) language sql
as $$

	insert into "История выдачи"("Дата",employee_id,"Издание","Номер издания","Выписан","Получен") values
	(date_var,emp_id,publication_var,num_of_publication,write_out,recieved);

$$;

drop function if exists delete_history(
 integer,
 integer,
 integer,
 integer,
 integer);
-- Функция удаления записи в таблице с историей получения изданий
create or replace function delete_history(
date_var date,
emp_id integer,
publication_var integer,
num_of_publication integer,
write_out integer,
recieved integer
) 
returns integer
language sql
as $$
with deleting as(
	delete from "История выдачи" where (publication_var<0 or publication_var="Издание") and
	(emp_id<0 or emp_id=employee_id) and
	("Номер издания"=num_of_publication or num_of_publication<0) and
	(write_out="Выписан" or write_out<0) and
	("Получен"=recieved or recieved<0) and
	("Дата"=date_var or date_var=null)
	 returning 1)
	 select count(*) from deleting;
$$;




-- Функция чтения из таблицы сотрудников
create or replace function read_employee(    
emp_id integer,
second_name varchar(64),
first_name varchar(64),
third_name varchar(64),
position_var varchar(64),
department varchar(64)
) returns table(
employee_id integer,
"Фамилия" varchar(64),
"Имя" varchar(64),
"Отчество" varchar(64),
"Должность" varchar(64),
"Подразделение" varchar(64)
) language sql
as $$
	select employee_id ,"Фамилия","Имя","Отчество","Должность","Подразделение" 
	from "Сотрудники" where (second_name='' or second_name="Фамилия") and
	(emp_id<0 or employee_id=emp_id) and
	("Имя"=first_name or first_name='') and
	(third_name="Отчество" or third_name='') and
	("Должность"=position_var or position_var='') and
	("Подразделение"=department or department='');
$$;



drop procedure if exists update_employee(emp_id integer,
 varchar(64),
 varchar(64),
 varchar(64),
 varchar(64),
 varchar(64));
 -- Процедура обновления записи в таблице с сотрудниками
create or replace procedure update_employee(
emp_id integer,
second_name varchar(64),
first_name varchar(64),
third_name varchar(64),
position_var varchar(64),
department varchar(64)
) language sql
as $$
 
	update "Сотрудники" set "Фамилия" = COALESCE(second_name, "Фамилия"),
    "Имя" = COALESCE(first_name, "Имя"),
    "Отчество" = COALESCE(third_name, "Отчество"),
    "Должность" = COALESCE(position_var, "Должность"),
	"Подразделение"= COALESCE(department,"Подразделение")
	where employee_id=emp_id;

$$;
 -- Процедура добавления записи в таблице с сотрудниками
drop procedure if exists insert_employee(emp_id integer,
 varchar(64),
 varchar(64),
 varchar(64),
 varchar(64),
 varchar(64));
create or replace procedure insert_employee(

second_name varchar(64),
first_name varchar(64),
third_name varchar(64),
position_var varchar(64),
department varchar(64) 
) language sql
as $$
	insert into "Сотрудники"("Фамилия","Имя","Отчество" ,"Должность","Подразделение") 
	values (second_name,first_name,third_name,position_var,department);
$$;
 -- Функция удаления записи в таблице с сотрудниками
drop function if exists delete_employee( integer,
 varchar(64),
 varchar(64),
 varchar(64),
 varchar(64),
 varchar(64));
create or replace function delete_employee(
emp_id integer,
second_name varchar(64),
first_name varchar(64),
third_name varchar(64),
position_var varchar(64),
department varchar(64)
) 
returns  integer
language sql
as $$
with deleting as (
	delete from "Сотрудники" where (second_name='' or second_name="Фамилия") and
	(emp_id<0 or employee_id=emp_id) and
	("Имя"=first_name or first_name='') and
	(third_name="Отчество" or third_name='') and
	("Должность"=position_var or position_var='') and
	("Подразделение"=department or department='')
	 returning 1)
	 select count(*) from deleting

$$;


-- Функция чтения из таблицы доставок
create or replace function read_delivery( 
	date_var date,
	del_id integer,
	type_var varchar(64)
) returns table(
delivery_id integer,
"Тип" varchar(64),
"Дата" DATE
) language sql
as $$
	select delivery_id ,"Тип","Дата"
	from "Доставка" where
	(del_id<0 or del_id=delivery_id) and
	("Тип"=type_var or type_var='') and
	(date_var is null or date_var="Дата");
$$;


-- Процедура обновления записи в таблице с доставками
create or replace procedure update_delivery( 
	date_var date,
	del_id integer,
	type_var varchar(64) 
) language sql
as $$ 
	update "Доставка" set 
	"Дата" = COALESCE(date_var,"Дата"),
    "Тип"= COALESCE(type_var, "Тип")
	where delivery_id=del_id;
$$;

-- Процедура добавления записи в таблице с доставками
create or replace procedure insert_delivery( 
	date_var date,
	type_var varchar(64) 
) language sql
as $$

	insert into "Доставка"("Тип","Дата") values
	(type_var,date_var);

$$;


-- Функция удаления записи в таблице с доставками
create or replace function delete_delivery( 
	date_var date,
	del_id integer,
	type_var varchar(64)
) 
returns integer
language sql
as $$
with deleting as(
	delete from "Доставка" where 
	(del_id<0 or del_id=delivery_id) and
	("Тип" like concat(type_var,'%') or type_var='') and
	(date_var is null or "Дата" = date_var) 
	 returning 1)
	 select count(*) from deleting;
$$;




-- Функция просмотра списка всех изданий, выписанных на заданный год – сначала журналы,  затем газеты, стоимость каждого издания на период подписки, период подписки.
create or replace function  printings_for_year()
returns table(
"Название" varchar(64),
"Индекс" integer,
"Периодичность  выхода" integer,
"Тип" varchar(64),
"Дата начала" DATE,
"Период" integer,
"Стоимость на период подписки" integer
) language sql
as $$
select t1."Название",t1."Индекс",t1."Периодичность  выхода",t1."Тип",t2."Дата начала",t2."Период",t2."Стоимость"*t2."Период" as full_price
from "Издания" t1 join "Подписки" t2 on t2."Индекс издания"=t1."Индекс" where extract(year from t2."Дата начала") = extract(year from now()) order by "Тип" desc;
$$;


-- функция просмотра списка изданий, которые не были получены в течение предыдущих двух  месяцев – дата формирования отчета, список изданий – название, дата подписки,  
-- периодичность, количество неполученных номеров
drop function if exists unrecieved_printings_for_two_months();
create or replace function  unrecieved_printings_for_two_months()
returns table(
"Название" varchar(64),
"Периодичность  выхода" integer,
"Тип" varchar(64),
"Дата начала" DATE,
"Период" integer,
"Количество неполученных номеров" integer
) language sql
as $$
with amount_of_unrecieved as(
	select t2."Название",count(t1.*) as "Количество неполученных" from "История выдачи" t1 
	join "Издания" t2 on t1."Издание"=t2."Индекс" where t1."Выписан"=1 and t1."Получен"=0 group by t2."Название")
select t1."Название",t1."Периодичность  выхода",t1."Тип",t2."Дата начала",t2."Период",t3."Количество неполученных"
	from "Издания" t1 join "Подписки" t2 on t2."Индекс издания"=t1."Индекс" join amount_of_unrecieved t3 on t1."Название"=t3."Название" 
	where (2>extract(month from age(now(),t2."Дата начала")) and extract(year from t2."Дата начала") = extract(year from now())) 
	or (extract(year from t2."Дата начала")+1 = extract(year from now()) and extract(month from t2."Дата начала") >= extract(month from now()))
	order by "Тип" desc;
$$;


-- Функция просмотра ФИО сотрудника подразделения, оформившего получение заданного  издания на заданный месяц. 

create or replace function employees_by_month_and_department(
department varchar(64),
month_year date,
name_of_printing varchar(64)
)
returns table (
emp_id integer,
"ФИО" varchar(64),
"Должность" varchar(64),
"Подразделение" varchar(64)
) language sql
as $$
	select t1.employee_id,concat(t1."Фамилия",t1."Имя",t1."Отчество"),t1."Должность",t1."Подразделение" 
	from "Сотрудники" t1 join  "Подписки" t2 on t1.employee_id=t2.employee_id 
	join "Издания" t3 on t2."Индекс издания"=t3."Индекс"
	where  month_year >= t2."Дата начала"
  and month_year <= t2."Дата окончания" and 
	t1."Подразделение"=department and t3."Название" like concat('%',name_of_printing,'%');

$$;

-- Функция проверки дат начала и конца подписки
create or replace function check_subscription_dates() 
returns trigger language plpgsql 
as $$ 
begin 
if new."Дата окончания" < new."Дата начала" then 
raise exception 'Дата окончания (%) не может быть раньше даты начала (%)', new."Дата окончания", new."Дата начала"; 
end if; 
return new; 
end; 
$$; 

-- Триггер на проверку дат подписки
create or replace trigger trg_check_dates before insert or update on "Подписки" 
for each row execute function check_subscription_dates();