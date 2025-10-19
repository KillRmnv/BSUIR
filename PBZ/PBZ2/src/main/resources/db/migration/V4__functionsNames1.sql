
drop table if exists functions_by_class_name;
create table if not exists functions_by_class_name(
class_name varchar(256) primary key,
create_procedure varchar(256),
read_function varchar(256),
update_procedure varchar(256),
delete_function varchar(256),
read_page_function varchar(256)
);

create or replace function get_function_name(
class_name_var varchar(256),
type_of_operation varchar(1)
)
returns varchar(256) language sql
as $$
select case
when type_of_operation='c' or type_of_operation='C'  then create_procedure
when type_of_operation='r' or type_of_operation='R' then read_function
when type_of_operation='u' or type_of_operation='U' then update_procedure
when type_of_operation='d' or type_of_operation='D' then delete_function
when type_of_operation='rp' or type_of_operation='RP' then read_page_function
end
from functions_by_class_name where class_name=class_name_var;
$$;

insert into functions_by_class_name
(class_name, create_procedure, read_function, update_procedure, delete_function,read_page_function)
values
('Subscription', 'insert_subsription(?,?,?::date,?::date,?,?,?)', 'read_subscription(?,?,?::date,?::date,?,?,?)', 'update_subscription(?,?,?::date,?::date,?,?,?)', 
'delete_subscription(?,?,?::date,?::date,?,?,?)','read_subscription_page(?,?)'),

('HistoryRecord', 'insert_history(?::date,?,?,?,?,?)', 'read_history(?::date,?,?,?,?,?)', 'update_history(?::date,?,?,?,?,?)', 
'delete_history(?::date,?,?,?,?,?)','read_history_page(?,?)'),

('Employee', 'insert_employee(?,?,?,?,?)', 'read_employee(?,?,?,?,?,?)', 'update_employee(?,?,?,?,?,?)',
'delete_employee(?,?,?,?,?,?)','read_employee_page(?,?)'),

('Printing', 'insert_printing', 'read_printing', 'update_printing', 'delete_printing','read_printing_page(?,?)'),

('Delivery', 'insert_delivery(?::date,?)', 'read_delivery(?::date,?,?)', 'update_delivery(?::date,?,?)', 'delete_delivery(?::date,?,?)','read_delivery_page(?,?)');
