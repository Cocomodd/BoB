from src.classes.db import db


c = db.get_cursor()
c.execute('''CREATE TABLE tweets (id int)''')
