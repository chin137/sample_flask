#Basic  Flask code to take data and save it into SQLite database that comes in built with python

from flask  import Flask, render_template, request
import sqlite3 
app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")


@app.route("/del")
def dele():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("delete from students")
	con.commit()
	con.close()
	return "All records have been deleted sucessfully!"


@app.route("/new")
def newrec():
	return render_template("add.html")


@app.route("/addrec",methods =["POST","GET"])
def addrec():
	if request.method =="POST":
		roll = request.form["ro"] 
		name = request.form["nm"] 
		age = request.form["ag"] 
		con = sqlite3.connect("database.db")
		cur = con.cursor()
		cur.execute('''INSERT INTO students  
               VALUES (?,?,?)''',(roll,name,age))
		con.commit()
		con.close()
		return "A record has been added sucessfully!"


@app.route("/data")
def getrec():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	res = cur.execute("select * from students")
	rows = res.fetchall()
	print(rows)
	con.close()
	return render_template("list.html",rows=rows) 

@app.route("/up")
def uprec():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("update students set age = 30")
	con.commit()
	con.close()
	return "All records have been updated sucessfully!"



if __name__ == "__main__":
	app.run()	







