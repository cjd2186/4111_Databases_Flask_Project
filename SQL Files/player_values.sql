CREATE TABLE player
	(person_id varchar(10)not null unique,
	 name varchar(40),
	 email varchar(40),
	 phone varchar(10),
 position varchar (20),
	 height int,
 weight int,
	 draft_class date,
	 passing_yds int,
	 rushing_yds int,
	 receiving_yds int,
	 total_tds int,
	 field_goals int,
	 xps int,
	 string int,
	 college varchar (20),
	 injury_status varchar (10),
     primary key (person_id),
	 foreign key (person_id) references person);

INSERT INTO player(person_id, name, email, phone, position, height, weight, draft_class, passing_yds, rushing_yds, receiving_yds,
	 total_tds, field_goals, xps, string, college, injury_status)
VALUES
('PL001', 'patrick_mahomes', 'pmahomes@chiefs.com', '5555550001', 'quarterback', '75', '230', '2017', '5097', '308', '0', '40', '0', '0', '1', 'texas_tech', 'healthy'),
('PL002', 'josh_allen', 'jallen@bills.com', '5555550002', 'quarterback', '77', '237', '2018', '4544', '421', '0', '43', '0', '0', '1', 'wyoming', 'healthy'),
('PL003', 'matthew_stafford', 'mstafford@rams.com', '5555550003', 'quarterback', '75', '220', '2009', '4600', '41', '0', '27', '0', '0', '1', 'georgia', 'healthy'),
('PL004', 'lamar_jackson', 'ljackson@ravens.com', '5555550004', 'quarterback', '74', '212', '2018', '2757', '1005', '0', '26', '0', '0', '1', 'louisville', 'healthy'),
('PL005', 'aaron_rodgers', 'arodgers@packers.com', '5555550005', 'quarterback', '74', '225', '2005', '4299', '149', '0', '40', '0', '0', '1', 'california', 'healthy'),
('PL006', 'jared_goff', 'jgoff@lions.com', '5555550006', 'quarterback', '76', '222', '2016', '4635', '92', '0', '22', '0', '0', '1', 'california', 'healthy'),
('PL007', 'saquon_barkley', 'sbarkley@giants.com', '5555550007', 'running_back', '72', '233', '2018', '0', '34', '355', '6', '0', '0', '1', 'penn_state', 'injured'),
('PL008', 'jalen_hurts', 'jhurts@eagles.com', '5555550008', 'quarterback', '73', '223', '2020', '2077', '784', '0', '22', '0', '0', '1', 'oklahoma', 'healthy'),
('PL009', 'joe_burrow', 'jburrow@bengals.com', '5555550009', 'quarterback', '76', '216', '2020', '4332', '142', '0', '16', '0', '0', '1', 'lsu', 'healthy'),
('PL010', 'mike_evans', 'mevans@buccaneers.com', '5555550010', 'wide_receiver', '77', '231', '2014', '0', '0', '1061', '13', '0', '0', '1', 'texas_a&m', 'healthy'),
('PL011', 'george_kittle', 'gkittle@49ers.com', '5555550011', 'tight_end', '76', '250', '2017', '0', '0', '634', '4', '0', '0', '1', 'iowa', 'healthy'),
('PL012', 'jordan_love', 'jlove@packers.com', '5555550012', 'quarterback', '76', '219', '2020', '0', '0', '0', '0', '0', '0', '2', 'utah_state', 'healthy'),
('PL013', 'chris_godwin', 'cgodwin@buccaneers.com', '5555550013', 'wide_receiver', '73', '209', '2017', '0', '0', '840', '7', '0', '0', '1', 'penn_state', 'injured'),
('PL014', 'darius_slayton', 'dslayton@giants.com', '5555550014', 'wide_receiver', '73', '190', '2019', '0', '0', '751', '3', '0', '0', '1', 'auburn', 'healthy'),
('PL015', 'geno_smith', 'gsmith@seahawks.com', '5555550015', 'quarterback', '75', '221', '2013', '0', '96', '0', '1', '0', '0', '2', 'west_virginia', 'healthy');

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