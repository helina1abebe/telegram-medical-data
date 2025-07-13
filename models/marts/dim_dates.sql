with calendar as (
  -- Change the date range as needed
  select 
    generate_series(
      '2020-01-01'::date, 
      '2030-12-31'::date, 
      interval '1 day'
    )::date as date
)

select
  date,
  to_char(date, 'YYYYMMDD')::int as date_id,
  extract(year from date)::int as year,
  extract(month from date)::int as month,
  extract(day from date)::int as day,
  to_char(date, 'Day') as weekday,
  case when extract(dow from date) in (0, 6) then true else false end as is_weekend
from calendar
