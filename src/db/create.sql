CREATE TABLE user
(
  name varchar(100),
  email varchar(100),
  id INTEGER PRIMARY KEY AUTOINCREMENT
);
CREATE TABLE tournament
(
  name varchar(100),
  checker varchar(100),
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  timelimit REAL,
  start_time DATETIME,
  end_time DATETIME
);

CREATE TABLE participants
(
  FOREIGN KEY (uid) REFERENCES user(id),
  FOREIGN KEY (tid) REFERENCES tournament(id),
  PRIMARY KEY (uid, tid)
);

CREATE TABLE solution
(
  FOREIGN KEY (uid, tid) REFERENCES participants(uid, tid),
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  build_status INTEGER,
  time DATETIME
);

CREATE TABLE game
(
  FOREIGN KEY (solution1) references solution(id),
  FOREIGN KEY (solution2) references solution(id),
  points1 INTEGER,
  points2 INTEGER,
  log TEXT
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  FOREIGN KEY (run) REFERENCES run(id)
);

CREATE TABLE run
(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  FOREIGN KEY (tid) REFERENCES tournament(id),
  timestart DATETIME
);


