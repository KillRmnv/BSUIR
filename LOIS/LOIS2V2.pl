% Лабораторная работа №2 по дисциплине "Логические основы интеллектуальных систем"
% Выполнена студентом группы 321701 БГУИР:
% - Романов Кирилл Викторович
% Вариант: 13

% Данный файл является исходным кодом к программе, решающий следующую задачу:

% Задача с трассами. Поменять местами сферы и звёзды. 
% Фишки можно перемещать из одной позиции в другую, по изображенным линиям, если целевая позиция свободна от других фишек. 

% Источники:
% 1. Логические основы интеллектуальных систем. Практикум : учеб.- метод. пособие / В. В. Голенков [и др.].
% – Минск : БГУИР, 2011. – 70 с. : ил. ISBN 978-985-488-487-5.
% 2. SWI Prolog [Электронный ресурс]. -- Режим доступа https://www.swi-prolog.org/

road(6,3). road(3,6).
road(4,1). road(1,4).
road(8,5). road(5,8).
road(1,6). road(6,1).
road(3,8). road(8,3).
road(7,4). road(4,7).
road(5,2). road(2,5).
road(7,2). road(2,7).

circle(c1). circle(c2).
star(s1). star(s2).
obj(X) :- star(X).
obj(X) :- circle(X).

:- dynamic pos/2,prevPos/2,curr_pos/1,force/1.

pos(s1,1).
pos(s2,3).
pos(c1,5).
pos(c2,7).

prevPos(c2,7).
prevPos(c1,5).
prevPos(s1,1).
prevPos(s2,3).

curr_pos([pos(s1,1),pos(s2,3),pos(c1,5),pos(c2,7)]).
goal_pos([goal(star,5), goal(star,7), goal(circle,1), goal(circle,3)]).

goal(Obj,Pos):-
    goal_pos(Goals),
    member(goal(Type,Pos), Goals),
    (pos(Obj,Pos), call(Type, Obj)).

globalGoal :-
    goal_pos(Goals),
    forall(member(goal(Type,Pos), Goals),
           (pos(Obj,Pos), call(Type, Obj))).

update_curr_pos :-
    retractall(curr_pos(_)),
    findall(pos(Obj, Pos), pos(Obj, Pos), NewCurr),
    assert(curr_pos(NewCurr)).

solve:-
    globalGoal,
    write("solved"),nl,!.  

solve:-
    curr_pos(Objs),
    maplist(try_move, Objs),
    update_curr_pos,
    solve.

try_move(pos(Obj,_)) :-
        move(_, _, Obj), !.
    try_move(_).  
    
check_for_next_move(To):-
    pos(AnthrObj,To),
    goal(AnthrObj,To),
    \+force(AnthrObj),
    road(To,AnthrTo),
    assert(force(AnthrObj)),
    move(AnthrObj,To,AnthrTo),
    retract(force(AnthrObj)).
    
println(Obj,Fr,To):-
    string_concat("Object: ", Obj, String),
    string_concat(String," moved from position:",String1),
    string_concat(String1,Fr,String2),
    string_concat(String2," to ",String3),
    string_concat(String3,To,String4),
    write(String4),
    nl.

move(Fr,To,Obj):-
        road(Fr,To),
        pos(Obj,Fr), 
        \+ prevPos(Obj,To),     
        \+ globalGoal,
        (\+ goal(Obj,Fr);force(Obj)), 
        (check_for_next_move(To);          
        \+ pos(_,To)),           
        retract(pos(Obj,Fr)),   
        assert(pos(Obj,To)),    
        prevPos(Obj,Prev),
        retract(prevPos(Obj,Prev)),
        assert(prevPos(Obj,Fr)),
        println(Obj,Fr,To).

move(_).