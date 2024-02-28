CREATE TABLE coaches 
	(person_id varchar(10),
	 name varchar(40),
	 primary key (person_id, name),
	 foreign key (person_id) references coach,
	 foreign key (name) references team);

INSERT INTO coaches (person_id, name)
VALUES
  ('HC001', 'giants'),
  ('HC002', 'cowboys'),
  ('HC003', 'eagles'),
  ('HC004', 'commanders'),
  ('HC005', 'cardinals'),
  ('HC006', 'rams'),
  ('HC007', '49ers'),
  ('HC008', 'seahawks'),
  ('HC009', 'falcons'),
  ('HC010', 'panthers'),
  ('HC011', 'panthers'),
  ('HC012', 'saints'),
  ('HC013', 'buccaneers');


    --giants: brian_daboll
--cowboys: mike_mccarthy
--eagles: nick_sirianni
--commanders: ron_rivera
--cardinals: kliff_kingsbury
--rams: sean_mcvay
--49ers: kyle_shanahan
--seahawks: pete_carroll
--falcons: arthur_smith
--panthers: matt_rhule  former_hc
--panthers: steve_wilks interm_hc
---saints: dennis_allen
--buccaneers: todd_bowles