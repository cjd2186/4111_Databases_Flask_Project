CREATE TABLE player_contract
	(term varchar (20)not null,
	 amount int,
	 start_year int,
	 person_id varchar (40),
    primary key (term, person_id),
    foreign key (person_id) references player ON DELETE CASCADE);

INSERT INTO player_control(contract_id, term, amount, start_year, person_id)
VALUES
patrick_mahomes
josh_allen
matthew_stafford
lamar_jackson
aaron_rodgers
jared_goff
saquon_barkley
jalen_hurts
joe_burrow
mike_evans
george_kittle
jordan_love
chris_godwin
darius_slayton
geno_smith


INSERT INTO player_contract(contract_id,term, amount, start_year, person_id)
VALUES
('CPL001', '10', '450000000', '2022', 'PL001'),
('CPL002', '8', '258000000', '2022', 'PL002'),
('CPL003', '4', '106000000', '2021', 'PL003'),
('CPL004', '5', '160000000', '2019', 'PL004'),
('CPL005', '4', '134000000', '2020', 'PL005'),
('CPL006', '4', '106000000', '2021', 'PL006'),
('CPL007', '4', '31000000', '2020', 'PL007'),
('CPL008', '4', '6805704', '2020', 'PL008'),
('CPL009', '4', '34200000', '2020', 'PL009'),
('CPL0010', '7', '93000000', '2020', 'PL010'),
('CPL0011', '5', '75000000', '2020', 'PL011'),
('CPL0012', '4', '12334076', '2022', 'PL012'),
('CPL0013', '1', '15500000', '2021', 'PL013'),
('CPL0014', '3', '6300000', '2019', 'PL014'),
('CPL0015', '2', '4250000', '2021', 'PL015');

Average player salary for quarterbacks
SELECT avg(CAST(pc.amount as int)/ CAST(pc.term as int)) as average_salary_for_qb
FROM player_contract pc, player p
WHERE p.position= 'quarterback' AND pc.person_id = p.person_id

output the names and home-stadiums of all players who have more than 1000 passing yards and make above average league salary.

SELECT p.name, s.name 
FROM ()

SELECT p.name, s.name
FROM player p, plays_for pf, stadium s, team t, plays_in pi, player_contract pc,
(SELECT avg(CAST(pc.amount as int)/ CAST(pc.term as int)) as average_salary_for_qb
FROM player_contract pc, player p
WHERE p.position= 'quarterback' AND pc.person_id = p.person_id) as salary
WHERE p.person_id= pf.person_id AND pf.name=t.name AND t.city=s.city AND p.passing_yds > 1000
GROUP BY p.name, s.name
HAVING CAST(pc.amount as int)/ CAST(pc.term as int) > CAST(salary as int)


output the names and home-stadiums of all players who have more than 1000 passing yards
SELECT p.name, s.name
FROM player p, plays_for pf, stadium s, team t, plays_in pi
WHERE p.person_id= pf.person_id AND pf.name=t.name AND t.city=s.city AND p.passing_yds > 1000
GROUP BY p.name, s.name