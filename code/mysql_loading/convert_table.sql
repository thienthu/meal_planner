-- create table convert_unit as
(
with a as 
(SELECT distinct(measure_unit) as measure_unit FROM recipedb.measure 
where measure_unit is not null
)

select measure_unit as unit, 
		case when measure_unit = 'cup' then 125  
			when measure_unit = 'lb' then 453.56
            when measure_unit = 'ml' then 1
            when measure_unit = 'ounce' then 28.35
            when measure_unit = 'pint' then 473
            when measure_unit = 'tablespoon' then 14.18
			when measure_unit = 'tbsp' then 7.81
            when measure_unit = 'teaspoon' then 5.6
            when measure_unit = 'dozen' then 12
            when measure_unit = 'g' then 1 
            else null end as amount,
		case when measure_unit = 'cup' then 'g'  
			when measure_unit = 'lb' then 'g'
            when measure_unit = 'ml' then 'g'
            when measure_unit = 'ounce' then 'g'
            when measure_unit = 'pint' then 'g'
            when measure_unit = 'tablespoon' then 'g'
			when measure_unit = 'tbsp' then 'g'
            when measure_unit = 'teaspoon' then 'g'
            when measure_unit = 'g' then 'g' 
            else null end as convert_unit		
from a
);