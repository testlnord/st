import os
import sqlite3
import config

if os.path.exists(os.path.join(config.db_path, config.db_name)):
    os.remove(os.path.join(config.db_path, config.db_name))

with sqlite3.connect(os.path.join(config.db_path, config.db_name)) as conn:
    c = conn.cursor()
    with open(os.path.join(config.db_path, config.db_creation_script)) as s_file:
        creation_script = s_file.read()
        c.executescript(creation_script)
