from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL





app=Flask(__name__,static_url_path='/static', static_folder='static')


app.secret_key='secret123'


#Mysql Connection

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='12345'
app.config['MYSQL_DB']='login'


mysql=MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():   
    return render_template("dashboard.html", username=session['username'])



@app.route("/login", methods=['GET','POST'])

def login():
    if request.method=='POST':
        UD=request.form
        username=UD['username']
        password=UD['password']
        cur=mysql.connection.cursor()
        cur.execute("SELECT * FROM form WHERE name=%s AND password=%s",(username,password))
        record = cur.fetchone()
        cur.connection.commit()
        cur.close()
        if record:
            session['logged_in']=True
            session['username']=record[1]
            return redirect(url_for('dashboard'))
        else:
            msg="Invalid Username or Password"
            return render_template("index.html", msg=msg)

    return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    if request.method=='POST':
        UD=request.form
        name=UD['name']
        email=UD['email']
        password=UD['password']
        location=UD['location']
        dob=UD['dob']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO form(name,email,password,location,dob) VALUES(%s,%s,%s,%s,%s)",(name,email,password,location,dob))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))
    return render_template("register.html")

@app.route('/users')
def users():
    cur=mysql.connection.cursor()
    result=cur.execute("SELECT * FROM form")
    if result>0:
        users=cur.fetchall()
        return render_template("users.html", users=users)
    else:
        msg="No Users Found"
        return render_template("users.html", msg=msg)
    cur.close()

if __name__=="__main__":
    app.run(debug=False,host='0.0.0.0')

        


