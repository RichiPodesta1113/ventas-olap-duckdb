-- Datos sintéticos reproducibles. Una fila representa un pedido de una categoría.
create table sales as
with source as (
    select i, hash(i, 'month') % 100003 % 12 as m, hash(i, 'region') % 100019 % 4 as r,
           hash(i, 'category') % 100043 % 3 as c, 1 + hash(i, 'units') % 5 as quantity
    from range(120000) as ids(i)
)
select i as order_id,
       strftime(date '2025-01-01' + m::int * interval '1 month', '%Y-%m') as month,
       ['Centro', 'Norte', 'Oriente', 'Sur'][r::bigint + 1] as region,
       ['Electrónica', 'Hogar', 'Ropa'][c::bigint + 1] as category,
       quantity as units,
       quantity * (1500 + c * 2400 + hash(i, 'price') % 10000) as revenue_cents
from source;

create table cube as
select month, region, category, count(*) as orders,
       sum(revenue_cents) as revenue_cents, sum(units) as units
from sales
group by month, region, category;
