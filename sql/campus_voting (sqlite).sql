-- noinspection SqlNoDataSourceInspectionForFile

CREATE TABLE 'aspirant' (
  'aspirant_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'voter_id' INTEGER NOT NULL,
  'aspirant_photo' longtext NOT NULL,
  FOREIGN KEY ('voter_id') REFERENCES 'voter' ('voter_id')
) ;


CREATE TABLE 'election' (
  'election_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'election_name' varchar(255) NOT NULL,
  'start_timestamp' timestamp NOT NULL DEFAULT current_timestamp(),
  'end_timestamp' timestamp NOT NULL DEFAULT current_timestamp()
) ;


CREATE TABLE 'school' (
  'school_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'school_name' varchar(255) NOT NULL
) ;


CREATE TABLE 'team' (
  'team_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'team_name' varchar(255) NOT NULL,
  'team_logo' longtext NOT NULL,
  'election_id' INTEGER NOT NULL,
  'chairman_id' INTEGER NOT NULL,
  'sec_gen_id' INTEGER NOT NULL,
  'treasurer_id' INTEGER NOT NULL,
  'blockchain_address' text NOT NULL,
  FOREIGN KEY ('chairman_id') REFERENCES 'aspirant' ('aspirant_id'),
  FOREIGN KEY ('election_id') REFERENCES 'election' ('election_id'),
  FOREIGN KEY ('sec_gen_id') REFERENCES 'aspirant' ('aspirant_id'),
  FOREIGN KEY ('treasurer_id') REFERENCES 'aspirant' ('aspirant_id')
) ;


CREATE TABLE 'vote' (
  'vote_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'election_id' INTEGER NOT NULL,
  'voter_id' INTEGER NOT NULL,
  FOREIGN KEY ('election_id') REFERENCES 'election' ('election_id'),
  FOREIGN KEY ('voter_id') REFERENCES 'voter' ('voter_id'),
  FOREIGN KEY ('voter_id') REFERENCES 'voter' ('voter_id')
) ;


CREATE TABLE 'voter' (
  'voter_id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  'voter_regno' varchar(50) NOT NULL,
  'school_id' INTEGER NOT NULL,
  'email' varchar(255) NOT NULL,
  'voter_password' varchar(255) NOT NULL,
  FOREIGN KEY ('school_id') REFERENCES 'school' ('school_id')
) ;