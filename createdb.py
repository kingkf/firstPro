#!/usr/bin/python

import sqlite3

def createdb():
    conn = sqlite3.connect('meituan.db')
    c = conn.cursor()
    c.execute('''create table stocks
    (searchNumber INTEGER, id INTEGER,
    name TEXT, region TEXT, price REAL,
    originalPrice REAL, discount REAL,
    saveMoney REAL, soldNumber INTEGER,
    sevenOrNot INTEGER, expireOrNot INTEGER,
    validStartTime TEXT, validEndTime TEXT,
    tips TEXT, greatness TEXT, mainImage TEXT)''')
    conn.commit()
    c.close()

if __name__ == "__main__":
    createdb()
