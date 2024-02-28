CREATE TABLE person
	(person_id varchar(10)not null unique,
	 name varchar(40),
	 email varchar(40),
	 phone varchar(10),
     primary key (person_id));

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
	 foreign key(person_id) references person,
	 foreign key(name) references person,
	 foreign key(phone) references person,
	 foreign key(email) references person);
	 
CREATE TABLE coach
	(person_id varchar(10)not null unique,
	 name varchar(40),
	 email varchar(40),
	 phone varchar(10),
	 role varchar(20),
	 record varchar(10),
     primary key (person_id),
	 foreign key(person_id) references person,
	 foreign key(name) references person,
	 foreign key(phone) references person,
	 foreign key(email) references person);
	 
CREATE TABLE player_contract
	(term varchar (20)not null,
	 amount int,
	 start_year date,
	 person_id varchar (40),
     primary key (term, person_id),
     foreign key (person_id) references player);

CREATE TABLE team
	(name varchar(40)not null unique,
	 city varchar(40),
	 conference varchar(20),
	 sb_wins int,
	 record varchar(10),
	 primary key (name));

CREATE TABLE mascot
	(mascot_name varchar (20) not null unique,
	 description varchar (20),
	 team_name varchar (40),
     primary key (mascot_name, team_name),
     foreign key (team_name) references team);

CREATE TABLE stadium
	(name varchar(40) not null unique,
	 city varchar(40),
	 playing_surface varchar(10),
	 seating_capacity int,
	 sponsor varchar(40),
	 primary key (name));
	 
CREATE TABLE represents
	(team_name varchar(40),
	 mascot_name varchar(40),
	 primary key (team_name, mascot_name),
     foreign key (team_name) references team,
     foreign key (mascot_name) references mascot);


CREATE TABLE game
	(date_time datetime,
	 score varchar(40),
	 winning_team varchar(10),
	 losing_team int,
	 weather_condition varchar(40),
     team_name varchar(40),
	 stadium_name varchar (40),
	 primary key (team_name, stadium_name),
	 foreign key (team_name) references team,
	 foreign key (stadium_name) references stadium);

CREATE TABLE plays_for 
	(person_id varchar(10),
	 name varchar(40),
	 primary key (person_id, name),
	 foreign key (person_id) references player,
	 foreign key (name) references team);

CREATE TABLE coaches 
	(person_id varchar(10),
	 name varchar(40),
	 primary key (person_id, name),
	 foreign key (person_id) references coach,
	 foreign key (name) references team);

CREATE TABLE plays_in
	(stadium_name varchar(40),
	 team_name varchar(40),
	 primary key (stadium_name, team_name),
	 foreign key (stadium_name) references stadium,
	 foreign key (team_name) references team);

CREATE TABLE signs 
	(person_id varchar(10),
	 term varchar(20),
	 primary key (person_id, term),
	 foreign key (person_id) references player,
	 foreign key (term) references player_contract);
