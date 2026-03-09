#Basic  Flask code to take data and save it into SQLite database that comes in built with python,CRUD Operations tutorial

from flask  import Flask, render_template, request, redirect,url_for,flash
import sqlite3 
from sqlite3 import IntegrityError, OperationalError, DatabaseError
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

		if not roll or not name or not age:
			flash(f"Please fill the entire form!","warning")
			return redirect(url_for("newrec"))

		try:
			roll = int(roll)
		except ValueError:
			flash(f"Please enter a numeric value for Roll number!","warning")
			return redirect(url_for("newrec"))

		try:
			age = int(age)
		except ValueError:
			flash(f"Please enter a numeric value for Age!","warning")
			return redirect(url_for("newrec"))


		with get_db_connection() as con:
			cur = con.cursor()
			try :
				cur.execute('''INSERT INTO students  
		               VALUES (?,?,?)''',(roll,name,age))
			except IntegrityError:
				flash(f"Roll number already exists","danger")
				return redirect(url_for("newrec"))
			except OperationalError as e:
				flash(f"Database error{e}","danger")
				return redirect(url_for("newrec"))
			except Exception as e:
				print(e)
				flash(f"Error{e}","danger")
				return redirect(url_for("newrec"))
			else:
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

		if not roll or not name or not age:
			flash(f"Please fill the entire form!","warning")
			return redirect(url_for("edit",id=id))

		try:
			roll = int(roll)
		except ValueError:
			flash(f"Please enter a numeric value for Roll number!","warning")
			return redirect(url_for("edit",id=id))

		try:
			age = int(age)
		except ValueError:
			flash(f"Please enter a numeric value for Age!","warning")
			return redirect(url_for("edit",id=id))

		with get_db_connection() as con:
			cur = con.cursor()
			try :
				cur.execute("update students set roll = ?, name = ?, age = ? where roll = ?",(roll,name,age,id))
			except IntegrityError:
				flash(f"Roll number already exists","danger")
			except OperationalError as e:
				flash(f"Database error{e}","danger")
			except Exception as e:
				print(e)
				flash(f"Error{e}","danger")
				return redirect(url_for("edit",id=id))
			else:		
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







