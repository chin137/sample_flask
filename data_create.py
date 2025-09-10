import sqlite3

conn = sqlite3.connect("database.db")
print("The database is opened succesfully!")

conn.execute('CREATE TABLE students (roll INT, name TEXT,age INT )')

print("Table has been created sucessfully!")

conn.close()