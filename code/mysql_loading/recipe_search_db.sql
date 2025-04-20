-- drop view recipe_search;
create view recipe_search as
(
with a1 as
(
SELECT t1.recipe_id, t1.measure_quantity, t1.measure_unit, t1.map_ingredient_name,
		t2.serving_size, t2.amount_g, t2.calories, t.unit, t.amount, t.convert_unit,
        case when t.convert_unit = 'g'  then t2.calories * t1.measure_quantity * t.amount / t2.amount_g
			 when t1.measure_quantity > 10 then t2.calories * t1.measure_quantity / t2.amount_g
			 else t2.calories * t1.measure_quantity / t2.serving_size end as ingredient_calory,
		case when t.convert_unit = 'g' then t1.measure_quantity * t.amount
			 when t1.measure_quantity > 10 then t1.measure_quantity
			 else t1.measure_quantity / t2.serving_size * t2.amount_g end as ingredient_gram
FROM measure t1
left join ingredient t2 on t1.map_ingredient_id = t2.id
left join convert_unit t on t1.measure_unit = t.unit
where t1.measure_quantity is not null
),
a2 as
(
select recipe_id, sum(ingredient_calory) as total_calory, sum(ingredient_gram) as total_gram, GROUP_CONCAT(map_ingredient_name) as ingredients from a1
group by recipe_id
),
a3 as
(
select name, area, id, case when (t3.time_cooking like "%m%") and t3.time_cooking < '30 m' then '< 30 minutes'
									   when (t3.time_cooking like "%m%") then '0.5 - 1 hour'
                                       when (t3.time_cooking like "%h%") then '1 - 2 hour'
                                       else '0.5 - 1 hour' end cooking_time, time_cooking, img_link, rating
from recipe as t3			
)
select  a2.recipe_id, a2.total_calory/total_gram*100 meal_calories, a2.ingredients, a3.name, a3.area, img_link,
        t4.category_pred as category, a3.cooking_time, rating
       
from a2
left join a3 on a2.recipe_id = a3.id 
left join recipe_category t4 on a2.recipe_id = t4.recipe_id
);


