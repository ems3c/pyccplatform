import sqlite3

def get_db_connection():
    conn = sqlite3.connect('db')
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()
vmquery = conn.execute('SELECT * FROM OPeratingSystems').fetchall()

print(vmquery[1]['OS_codename'])

conn.close()

