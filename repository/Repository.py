import sqlite3
from constants import DB

def getCursorAndConnection():
    conn = sqlite3.connect(DB.kuclass_db)
    conn.execute("PRAGMA foreign_keys = 1")
    c = conn.cursor()

    return c, conn