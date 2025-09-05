import sqlite3
import pickle
from datetime import datetime
from loguru import logger

# create table in the first run
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS CXLogin (
        Username TEXT PRIMARY KEY,
        Encpassword TEXT NOT NULL,
        Cookie BLOB NOT NULL,
        Time TEXT NOT NULL
    )
    ''')
conn.commit()
conn.close()

class DatabaseManager:
    def __enter__(self):
        self.conn = sqlite3.connect("data.db")
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
    
    def addCookie(self, username:str, encpassword:str, cookie):
        cookie = pickle.dumps(cookie)
        self.cursor.execute("SELECT * FROM CXLogin WHERE Username = ?", (username,))
        result = self.cursor.fetchone()
        currentTime = round(datetime.now().timestamp())
        if result is not None:
            self.cursor.execute('''
                UPDATE CXLogin SET Encpassword = ?, Cookie = ?, Time = ? WHERE Username = ?
            ''', (encpassword, cookie, currentTime, username))
        else:
            self.cursor.execute('''
                INSERT INTO CXLogin (Username, Encpassword, Cookie, Time) VALUES (?, ?, ?, ?)
            ''', (username, encpassword, cookie, currentTime))
        self.conn.commit()
        logger.info("信息已添加至数据库")

    def getCookie(self, username: str):
        self.cursor.execute("SELECT * FROM CXLogin WHERE Username = ?", (username,))
        result = self.cursor.fetchone()
        encpassword = result[1]
        cookie = pickle.loads( result[2])
        addTime = int(result[3])
        return {
            'addTime': addTime,
            'cookie': cookie,
            'encpassword': encpassword
        }
    
    def deleteCookie(self, username: str):
        self.cursor.execute("DELETE FROM CXLogin WHERE Username = ?", (username,))
        self.conn.commit()
        logger.info(f"已删除用户：{username}的Cookie")