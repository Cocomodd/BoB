import sqlite3

conn = sqlite3.connect('kitty.db')
c = conn.cursor()
c.execute('''CREATE TABLE tweets (id int)''')
