#Basic  Flask code to take data and save it into SQLite database that comes in built with python

from flask  import Flask, render_template, request, redirect,url_for
import sqlite3 
app = Flask(__name__)

#Basic routing for Home page 
@app.route("/")
def home():
	return render_template("index.html")

#Routing to handle deletion of one student
@app.route("/del/<int:id>")
def dele(id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	cur.execute("delete from students where roll = ?",(id,))
	con.commit()
	con.close()
	return redirect(url_for("getrec"))

#Routing for Adding a new student
@app.route("/new")
def newrec():
	return render_template("add.html")

#Routing for Entering Updated Student Details
@app.route("/edit/<int:id>")
def edit(id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	res = cur.execute("select * from students where roll = ?",(id,))
	row = res.fetchone()
	print(row)
	con.close()
	return render_template("upd.html",rows = row)	



#Routing for Handling new Student creation
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
		return redirect(url_for("getrec"))
		

#Routing for Editing Student details
@app.route("/updrec/<int:id>",methods =["POST","GET"])
def updrec(id):
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	if request.method =="POST":
		roll = request.form["ro"] 
		name = request.form["nm"] 
		age =  request.form["ag"] 
		con = sqlite3.connect("database.db")
		cur = con.cursor()
		cur.execute("update students set roll = ?, name = ?, age = ? where roll = ?",(roll,name,age,id))
		con.commit()
		con.close()
		return redirect(url_for("getrec"))
	


#Routing for Getting all the Student details
@app.route("/data")
def getrec():
	con = sqlite3.connect("database.db")
	cur = con.cursor()
	res = cur.execute("select * from students")
	rows = res.fetchall()
	print(rows)
	con.close()
	return render_template("list.html",rows=rows) 


if __name__ == "__main__":
	app.run()	







