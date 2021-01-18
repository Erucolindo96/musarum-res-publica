-- How many interpellations a given deputy made?
-- Deputy -- Interpellations count
select d.name, count(d_i.interpellation_id) as interpellations_count from deputy_interpellation as d_i
join deputy as d on d_i.deputy_id=d.id
group by d.id
order by interpellations_count desc


-- List all mentions of districts in interpellations
-- Deputy - Interpellation - Election district
select d.name, i_s.interpellation_id, c.district_number
from interpellation_settles as i_s
join settle as s on i_s.settle_id=s.id
join county as c on c.id=s.county_id and c.voivodeship_id=s.voivodeship_id
join deputy_interpellation as d_i on i_s.interpellation_id = d_i.interpellation_id
join deputy as d on d_i.deputy_id=d.id


-- List all unique interpellation -> district mentions and the number of times a district was mentioned in given interpellation
-- Deputy - Interpellation - Election district - Mention count
select d.name, i_s.interpellation_id, c.district_number, count(*) as mention_count
from interpellation_settles as i_s
join settle as s on i_s.settle_id=s.id
join county as c on c.id=s.county_id and c.voivodeship_id=s.voivodeship_id
join deputy_interpellation as d_i on i_s.interpellation_id = d_i.interpellation_id
join deputy as d on d_i.deputy_id=d.id
group by i_s.interpellation_id, c.district_number