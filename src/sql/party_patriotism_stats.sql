-- What part of interpellations concerns region? (PARTY)

drop view if exists party_all_interpellations_count
create view party_all_interpellations_count as
select party, count(*) as interpellations_count from (
    select d.party, d_i.interpellation_id from deputy_interpellation as d_i
    join deputy as d on d_i.deputy_id=d.id
    group by d.party, d_i.interpellation_id
)
group by party

drop view if exists party_patriotic_interpellations_count
create view party_patriotic_interpellations_count as
select party, count(*) as interpellations_count from (
    select d.party, d_i.interpellation_id from deputy_interpellation as d_i
    join deputy as d on d_i.deputy_id=d.id
    where exists (
        select 1 from interpellation_settles as i_s
        join settle as s on s.id=i_s.settle_id
        join county as c on c.id=s.county_id and c.voivodeship_id=s.voivodeship_id
        where c.district_number=d.district_number and i_s.interpellation_id=d_i.interpellation_id
    )
    group by d.party, d_i.interpellation_id
)
group by party

select * from party_all_interpellations_count
select * from party_patriotic_interpellations_count


-- Party name - Patriotic interpellations percentage
select a.party, p.interpellations_count as patriotic_interpellations, a.interpellations_count as all_interpellations,
printf("%.2f", (p.interpellations_count*1.0/a.interpellations_count)) as patriotic_to_all
from party_all_interpellations_count as a
join party_patriotic_interpellations_count as p on p.party=a.party
order by patriotic_to_all desc