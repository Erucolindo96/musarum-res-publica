-- Count of interpellations
select count(*) from interpellation

-- 10 most recent interpellations
select * from interpellation order by date(date) desc limit 10

-- Count of unique dates of interpellations
select count(*) from (select distinct date(date) from interpellation) as dates

-- Count of deputy table rows
select count(*) from deputy

-- Count of unique deputy names
select count(name) from (select distinct name from deputy) as names

-- Deputy names ascending
select distinct name from deputy order by name

-- 10 most recent interpellations and their authors
select i.id, i."date", GROUP_CONCAT(d.name, ', '), i.content from deputy_interpellation as di
join deputy as d on di.deputy_id=d.id
join interpellation as i on di.interpellation_id=i.id
group by i.id
order by date(i."date") desc
limit 10

-- Find given deputy interpellations
select i.id, i."date", d.name, i.content from deputy_interpellation as di
join deputy as d on di.deputy_id=d.id
join interpellation as i on di.interpellation_id=i.id
where d.name LIKE '%Święczkowski'
