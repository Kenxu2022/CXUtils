import sqlite3
import os

if os.path.exists("db/data.db"):
    conn = sqlite3.connect("db/data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM CXLogin")
    if "Nickname" not in [description[0] for description in cursor.description]:
        cursor.execute('''
            ALTER TABLE CXLogin ADD COLUMN Nickname TEXT NOT NULL DEFAULT ''
        ''')
        conn.commit()
    conn.close()
    