import sqlite3

conn = sqlite3.connect('data.db')

# 创建一个Cursor
c = conn.cursor()


def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = cursor.fetchone()
    return result is not None


if table_exists(conn, 'ssr'):
    print("表 'users' 存在。")
else:
    print("表 'users' 不存在。")
    c.execute('''CREATE TABLE IF NOT EXISTS users  
                 (user_id INTEGER, 
                 nickname TEXT NOT NULL,  
                 signtime TEXT NOT NULL,
                 stone INTEGER NOT NULL)''')
