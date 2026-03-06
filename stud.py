#Basic  Flask code to take data and save it into SQLite database that comes in built with python,CRUD Operations tutorial

from flask  import Flask, render_template, request, redirect,url_for,flash
import sqlite3 
app = Flask(__name__)
app.secret_key = "super_secret_key_1267"

# Helper function to reduce repetitive code
def get_db_connection():
    conn = sqlite3.connect("database.db")
    return conn

#Basic routing for Home page 
@app.route("/")
def home():
	return render_template("index.html")

#Routing for Getting all the Student details
@app.route("/data")
def getrec():
	with get_db_connection() as con:
		cur = con.cursor()
		res = cur.execute("select * from students")
		rows = res.fetchall()
		print(rows)
	return render_template("list.html",rows=rows) 	

#Routing for Adding a new student
@app.route("/new")
def newrec():
	return render_template("add.html")	


#Routing for Handling new Student creation
@app.route("/addrec",methods =["POST","GET"])
def addrec():
	if request.method =="POST":
		roll = request.form["ro"] 
		name = request.form["nm"] 
		age = request.form["ag"] 
		with get_db_connection() as con:
			cur = con.cursor()
			cur.execute('''INSERT INTO students  
	               VALUES (?,?,?)''',(roll,name,age))
			con.commit()
		flash("New Student record is added","success")	
		return redirect(url_for("getrec"))	




#Routing for Pre-populating the Student details
@app.route("/edit/<int:id>")
def edit(id):
	with get_db_connection() as con:
		cur = con.cursor()
		res = cur.execute("select * from students where roll = ?",(id,))
		row = res.fetchone()
		print(row)
	return render_template("upd.html",rows = row)		
	


#Routing for Saving the modified Student details
@app.route("/updrec/<int:id>",methods =["POST","GET"])
def updrec(id):
	if request.method =="POST":
		roll = request.form["ro"] 
		name = request.form["nm"] 
		age =  request.form["ag"] 
		with get_db_connection() as con:
			cur = con.cursor()
			cur.execute("update students set roll = ?, name = ?, age = ? where roll = ?",(roll,name,age,id))
			con.commit()
		flash("Student record is Modified!","info")	
		return redirect(url_for("getrec"))		

#Routing to handle deletion of one student
@app.route("/del/<int:id>")
def dele(id):
	with get_db_connection() as con:
		cur = con.cursor()
		cur.execute("delete from students where roll = ?",(id,))
		con.commit()
	flash("Student record is Deleted!","success")	
	return redirect(url_for("getrec"))


if __name__ == "__main__":
	app.run(debug = True)	







