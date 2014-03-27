pragma foreign_keys = on;

CREATE TABLE user
(
  name varchar(100),
  email varchar(100),
  id INTEGER PRIMARY KEY 
);
CREATE TABLE tournament
(
  name varchar(100),
  checker varchar(100),
  id INTEGER PRIMARY KEY ,
  timelimit REAL,
  start_time DATETIME,
  end_time DATETIME
);

CREATE TABLE participants
(
  user_id INTEGER,
  tour_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user(id) on delete cascade,
  FOREIGN KEY (tour_id) REFERENCES tournament(id)  on delete cascade ,
  PRIMARY KEY (user_id, tour_id)
);

CREATE TABLE solution
(
  user_id INTEGER,
  tour_id INTEGER,
  id INTEGER PRIMARY KEY ,
  build_status INTEGER,
  time DATETIME,
  FOREIGN KEY (user_id, tour_id) REFERENCES participants(uid, tid)
);
CREATE TABLE run
(
  id INTEGER PRIMARY KEY ,
  tour_id INTEGER,
  timestart DATETIME,
  FOREIGN KEY (tour_id) REFERENCES tournament(id)
);
CREATE TABLE game
(
  id INTEGER PRIMARY KEY ,
  solution1 INTEGER,
  solution2 INTEGER,
  points1 INTEGER,
  points2 INTEGER,
  run INTEGER,
  log TEXT,
  FOREIGN KEY (solution1) references solution(id),
  FOREIGN KEY (solution2) references solution(id),
  FOREIGN KEY (run) REFERENCES run(id)
);




