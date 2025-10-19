
-- 14 задание:Получить все такие пары номеров деталей, которые обе поставляются одновременно одним
-- поставщиком.
WITH subq AS (
SELECT 
    spj1."Д#" as "Деталь 1",
    spj2."Д#" as "Деталь 2"
FROM "Поставки SPJ" spj1
JOIN "Поставки SPJ" spj2 ON  spj1."П#" = spj2."П#"
WHERE spj1."Д#"<spj2."Д#" ) 
SELECT distinct("Деталь 1","Деталь 2") FROM subq;


-- 29. Получить номера проектов, полностью обеспечиваемых поставщиком П1.
with projects_by_amount_of_P as(
select "ПР#",count("П#") as amount from "Поставки SPJ" GROUP BY "ПР#"
)
SELECT spj."ПР#"
FROM "Поставки SPJ" spj join projects_by_amount_of_P p on spj."ПР#"=p."ПР#"
WHERE spj."П#" = 'П1' and p.amount=1
GROUP BY spj."ПР#"
;

-- 1. Получить полную информацию обо всех проектах.
SELECT j."ПР#", j."Имя ПР", j."Город",spj."П#",spj."Д#",spj."S" 
FROM "Проекты J" j JOIN "Поставки SPJ" spj ON j."ПР#"=spj."ПР#";

-- 9. Получить номера деталей, поставляемых поставщиком в Лондоне.
WITH sort_by_town AS (SELECT * FROM "Поставщики S" WHERE "Город"='Лондон')
SELECT DISTINCT spj."Д#" FROM "Поставки SPJ" spj JOIN sort_by_town lon ON spj."П#"=lon."П#" ; 

-- 18. Получить номера деталей, поставляемых для некоторого проекта со средним количеством
-- больше 320.
WITH prices AS(
SELECT DISTINCT "П#",AVG("S") as price FROM "Поставки SPJ" GROUP BY "П#")
SELECT DISTINCT spj."Д#",spj."П#" FROM "Поставки SPJ" spj JOIN prices p ON p."П#"=spj."П#" WHERE p.price>320;
-- 19. Получить имена проектов, обеспечиваемых поставщиком П1.
SELECT DISTINCT j."Имя ПР" FROM "Проекты J" j
JOIN "Поставки SPJ" spj ON j."ПР#"=spj."ПР#" WHERE spj."П#"='П1';

-- 23. Получить номера поставщиков, поставляющих по крайней мере одну деталь, поставляемую по
-- крайней мере одним поставщиком, который поставляет по крайней мере одну красную деталь.
WITH details AS (
SELECT "Д#" FROM "Детали P" WHERE "Цвет"='Красный'),
 post AS(
SELECT DISTINCT spj."П#" FROM "Поставки SPJ" spj JOIN details d ON spj."Д#"=d."Д#"),
 details_post AS(
SELECT DISTINCT spj."Д#" FROM "Поставки SPJ" spj JOIN post p ON spj."П#"=p."П#"
)
SELECT DISTINCT spj."П#" FROM "Поставки SPJ" spj JOIN details_post d ON spj."Д#"=d."Д#";


-- 25. Получить номера проектов, город которых стоит первым в алфавитном списке городов.
WITH first_town AS(
SELECT "Город" FROM "Проекты J" ORDER BY "Город" ASC LIMIT 1)
SELECT j."ПР#" FROM "Проекты J" j JOIN first_town f ON f."Город"=j."Город";

-- 4. Получить все отправки, где количество находится в диапазоне от 300 до 750 включительно.
SELECT "П#", "Д#", "ПР#", "S" FROM "Поставки SPJ"
WHERE "S">=300 AND "S"<=750; 


-- 26. Получить номера проектов, для которых среднее количество поставляемых деталей Д1 больше,
-- чем наибольшее количество любых деталей, поставляемых для проекта ПР1.
WITH detaiL_amount AS(SELECT  "S" 
FROM "Поставки SPJ" WHERE "ПР#"='ПР1'
ORDER BY "S" LIMIT 1),
avg_amount AS(SELECT "П#",AVG("S") AS avr
FROM "Поставки SPJ" WHERE "Д#"='Д1' 
GROUP BY "П#")
SELECT DISTINCT spj."П#" FROM "Поставки SPJ" spj 
JOIN avg_amount aa ON aa."П#"=spj."П#" 
JOIN detail_amount d ON d."S"<aa.avr;