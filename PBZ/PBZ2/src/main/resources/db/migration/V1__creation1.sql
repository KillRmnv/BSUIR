create table if not exists public.Departments
(
    department_id serial primary key,
    department_name varchar(64) unique not null
);

create table if not exists public.PublicationTypes
(
    type_id serial primary key,
    type_name varchar(64) unique not null
);
CREATE TABLE IF NOT EXISTS Frequencies
(
    freq_id SERIAL PRIMARY KEY,
    freq_name VARCHAR(30) UNIQUE NOT NULL
        CHECK (freq_name IN ('ежедневно', 'еженедельно', 'ежемесячно', 'ежеквартально', 'раз в полгода'))
);
create table if not exists public.Employees
(
    employee_id serial primary key,
    second_name varchar(64) not null,
    first_name varchar(64) not null,
    third_name varchar(64) not null,
    position varchar(64) not null,
    department_id integer references Departments(department_id)
                                on delete set null
);

create table if not exists public.Printings
(
    name varchar(64) not null,
    index integer check (index > 0) primary key unique,
    freq_id INT NOT NULL REFERENCES Frequencies(freq_id)
        on delete set null,
    type_id integer default 1 references PublicationTypes(type_id)
        on delete set default
);
CREATE TABLE IF NOT EXISTS SubsPeriods (
                                           freq_id SERIAL PRIMARY KEY,
                                           freq_name VARCHAR(30) UNIQUE NOT NULL
                                               CHECK (freq_name IN ('год',  'полгода'))
);
create table if not exists public.Subs
(
    id             serial primary key,
    index_printing integer references Printings (index)
        on delete cascade,
    employee_id    integer references Employees (employee_id)
        on delete cascade,
    date_beg       date not null,
    date_end       date not null,
    period         integer default 1 references SubsPeriods(freq_id) on delete  set default not null,
    cost           integer check (cost > 0) not null
);

create table if not exists public.Circulation
(	id serial primary key,
     pub_id     integer references Printings(index) on delete cascade,
     amount     integer check (amount > 0),
     allocated_amount integer check ( allocated_amount>-1 ) default 0,
     num_of_pub integer check (num_of_pub > 0)
);

create table if not exists public.HistoryStates
(
    state_id   serial primary key,
    state_name varchar(128) not null
);

insert into public.HistoryStates (state_name)
values ('Выписано'), ('Получено');

create table if not exists public.History
(
    id              serial primary key,
    date_hist       date,
    subscription_id integer references Subs (id),
    num_pub         integer references Circulation(num_of_pub),
    state           integer references HistoryStates (state_id)
        on delete restrict,
    constraint fk_num_pub foreign key (num_pub)
        references Circulation (id)
        on delete no action,
    constraint chck_num_of_printing check (num_pub > 0)
);
create table if not exists DeliveryType(
                                           id serial primary key ,
                                           type_d varchar(128)
);
create table if not exists public.delivery
(
    delivery_id serial primary key,
    type_d      integer default 1 references DeliveryType(id) on delete set default ,
    address     varchar(128) not null,
    hist_id     integer references History (id) on delete cascade,
    expected_date date
);

create table if not exists public.Organization(
                                                  id serial primary key ,
                                                  name varchar(64),
                                                  base_address_for_delivery varchar(64),
                                                  type_of_delivery integer references DeliveryType(id)
);

-- drop table if exists History;
-- drop table if exists Subs;
-- drop table if exists delivery;
-- drop table if exists Employees;
-- drop table if exists Printings;