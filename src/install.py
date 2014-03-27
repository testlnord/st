import sqlite3
import config

with sqlite3.connect(config.db_path+config.db_name) as conn:
    c = conn.cursor()
    with open(config.db_path+config.db_creation_script) as s_file:
        creation_script = s_file.read()
        c.executescript(creation_script)

