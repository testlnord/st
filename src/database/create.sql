pragma foreign_keys = on;

CREATE TABLE IF NOT EXISTS user
(
  name varchar(100),
  email varchar(100),
  id INTEGER PRIMARY KEY,
  UNIQUE (name)
);
CREATE TABLE IF NOT EXISTS tournament
(
  name varchar(100),
  checker varchar(100),
  id INTEGER PRIMARY KEY ,
  timelimit REAL,
  start_time DATETIME,
  end_time DATETIME,
  UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS participants
(
  user_id INTEGER,
  tour_id INTEGER,
  FOREIGN KEY (user_id) REFERENCES user(id) on delete cascade,
  FOREIGN KEY (tour_id) REFERENCES tournament(id)  on delete cascade ,
  PRIMARY KEY (user_id, tour_id)
);

CREATE TABLE IF NOT EXISTS solution
(
  user_id INTEGER,
  tour_id INTEGER,
  id INTEGER PRIMARY KEY ,
  build_status INTEGER,
  runner_name VARCHAR(100),
  out_name VARCHAR(50),
  time DATETIME,
  FOREIGN KEY (user_id, tour_id) REFERENCES participants(user_id, tour_id)
);
CREATE TABLE IF NOT EXISTS run
(
  id INTEGER PRIMARY KEY ,
  tour_id INTEGER,
  timestart DATETIME,
  FOREIGN KEY (tour_id) REFERENCES tournament(id),
  UNIQUE (run_name)
);
CREATE TABLE IF NOT EXISTS game
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




