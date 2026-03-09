import sqlite3

conn = sqlite3.connect("database.db")
print("The database is opened succesfully!")

conn.execute('CREATE TABLE students (roll INT primary key, name TEXT,age INT )')
print("Table has been created sucessfully!")

#conn.execute('drop TABLE students')
#print("The table is deleted sucessfully!")
conn.close()