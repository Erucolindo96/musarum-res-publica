-- What part of interpellations concerns region?

drop view if exists deputy_all_interpellations_count
create view deputy_all_interpellations_count as
select d.id, d.name, d.party, count(d_i.interpellation_id) as interpellations_count from deputy_interpellation as d_i
join deputy as d on d_i.deputy_id=d.id
group by d.id
order by d.id

drop view if exists deputy_patriotic_interpellations_count
create view deputy_patriotic_interpellations_count as
select id, name, party, count(*) as interpellations_count from (
    select d.id, d.name, d.party, i_s.interpellation_id
    from interpellation_settles as i_s
    join settle as s on i_s.settle_id=s.id
    join county as c on c.id=s.county_id and c.voivodeship_id=s.voivodeship_id
    join deputy_interpellation as d_i on i_s.interpellation_id = d_i.interpellation_id
    join deputy as d on d_i.deputy_id=d.id
    where c.district_number=d.district_number
    group by d.id, i_s.interpellation_id
)
group by name
order by id


select * from deputy_all_interpellations_count
select * from deputy_patriotic_interpellations_count

-- Deputy id - Deputy name - Patriotic interpellations percentage
select a.name, a.party, p.interpellations_count as patriotic_interpellations, a.interpellations_count as all_interpellations,
printf("%.2f", (p.interpellations_count*1.0/a.interpellations_count)) as patriotic_to_all
from deputy_all_interpellations_count as a
join deputy_patriotic_interpellations_count as p on p.id=a.id
order by patriotic_to_all desc
limit 10

-- Deputy id - Deputy name - Patriotic interpellations percentage (at least 10 interpellations)
select a.name, a.party, p.interpellations_count as patriotic_interpellations, a.interpellations_count as all_interpellations,
printf("%.2f", (p.interpellations_count*1.0/a.interpellations_count)) as patriotic_to_all
from deputy_all_interpellations_count as a
join deputy_patriotic_interpellations_count as p on p.id=a.id
where a.interpellations_count >= 10
order by patriotic_to_all desc
limit 10