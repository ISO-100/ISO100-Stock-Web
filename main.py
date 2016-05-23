from flask import Flask, request, render_template, redirect, url_for, flash, session, json, jsonify
import os
import logging
from flaskext.mysql import MySQL
from logging.handlers import RotatingFileHandler
#For form class
from forms import RegistrationForm
#from user.models import User
from passlib.hash import sha512_crypt
# For preventing SQL Injection
from MySQLdb import escape_string as thwart
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from functools import wraps
#from datatables import DataTablesServer


app = Flask(__name__)

#mysql
mysql = MySQL()
app.config.from_object('settings')
mysql.init_app(app)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))
    return wrap

@app.route("/")
#@login_required
def index():
    if 'username' in session:
        return render_template("multi_tab.html",username=session['username'])
    else:
        return redirect(url_for("login"))

def valid_login(username,password):
    try:
        c = mysql.connect().cursor()
        c.execute("SELECT * FROM USER WHERE username ='%s'" %(username))
        data = c.fetchone()[2]
        if data and sha512_crypt.verify(password, data):
            return True
        else:
            return False
    except:
        return False
        
@app.route("/login",methods=['GET','POST'])
def login():
    error = None
    if request.method=="POST":
        if valid_login(
            request.form.get('username'),
            request.form.get('password')
        ):
            flash("Successfully logged in")
            session['logged_in'] = True
            session['username'] = request.form.get('username')
            return redirect(url_for('index'))
        else:
            error= "Incorrect username or password"
            app.logger.warning("Incorrect username and password for user (%s)", request.form.get('username'))
    return render_template("login2.html", error=error)

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('logged_in', False)
    return redirect(url_for('login'))

@app.route("/register", methods=['GET','POST'])
def register():
    remark = "Checkpoint Null"
    form = RegistrationForm(request.form)
    #remark = form.validate()
    
    if request.method == "POST":
        if form.validate():
            remark = "Checkpoint 2"
            username = form.username.data
            #password = form.password.data
            password = sha512_crypt.encrypt((str(form.password.data)))
            email = form.email.data
            # Check if the user exist
            remark = "Checkpoint 3"
            conn = mysql.connect()
            cursor = conn.cursor()
            x = cursor.execute("SELECT * FROM USER WHERE username = '%s'", (username))
            remark = "Checkpoint 4"
            if int(x) > 0:
                remark = "This username is existed, please choose another one."
                flash("This username is existed, please choose another one.")
                return render_template("register.html", form=form, remark=remark)
            else:
                cursor.execute("INSERT INTO USER (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
                #con.execute("INSERT OR REPLACE INTO stk_lst (stk_num, stk_name) VALUES(?,?)",(stock_num,stock_name))
                #cur.execute( "SELECT * FROM records WHERE email LIKE '%s'", search )
                #cursor.executemany('''INSERT INTO popularity      VALUES (%s, %s, %s)''', entries_list)
                conn.commit()
                conn.close()
                flash("Thanks for registering")
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for("index"))
    else:
        #flash(form.errors)
        #remark = 'Checkpoint 99'
        return render_template("register.html", form=form, remark=remark)

@app.route("/mysqltojson")
def mysqltojson():
    c = mysql.connect().cursor()
    c.execute("SELECT * FROM stk_lst")
    results = c.fetchall()
    tupletodic = { "data" : [[x[0], x[1]] for x in results] }
    return jsonify(tupletodic)

@app.route("/mysqltojson2")
def mysqltojson2():
    c = mysql.connect().cursor()
    c.execute("SELECT * FROM stk_prc")
    results = c.fetchall()
    RMB_code = '\xef\xbf\xa5'
    RMB_code = RMB_code.decode("utf8")
    tupletodic = { "data" : [[x[0], x[1], RMB_code + str(x[2]), RMB_code + str(x[3]),RMB_code + str(x[4]), RMB_code + str(x[5]),RMB_code + str(x[6]), "{:,}".format(int(x[9])),RMB_code + str("{:,}".format(int(x[10]))), x[11],x[12]] for x in results] }
    return jsonify(tupletodic)
    
@app.route("/mysqltojson3")
def mysqltojson3():
    c = mysql.connect().cursor()
    c.execute("SELECT * FROM co_qr")
    results = c.fetchall()
    RMB_code = '\xef\xbf\xa5'
    RMB_code = RMB_code.decode("utf8")
    tupletodic = { "data" : [[x[0], x[1],x[2], RMB_code + str(x[3]),RMB_code + str("{:,}".format(int(x[4]))), str(x[5]) + '%',RMB_code + str("{:,}".format(int(x[6]))), str(x[7]) + '%', x[8], str(x[9])+'%',x[10], str(x[11])+'%',x[12]] for x in results] }
    return jsonify(tupletodic)
    
@app.route("/mysqltojson4")
def mysqltojson4():
    c = mysql.connect().cursor()
    c.execute("SELECT * FROM co_er")
    results = c.fetchall()
    RMB_code = '\xef\xbf\xa5'
    RMB_code = RMB_code.decode("utf8")
    tupletodic = { "data" : [[x[0], x[1], x[2], x[3], x[4], x[5], RMB_code + str(x[6]), x[7]] for x in results] }
    return jsonify(tupletodic)

@app.route("/mysqltojson5")
def mysqltojson5():
    c = mysql.connect().cursor()
    c.execute("SELECT * FROM int_eps")
    results = c.fetchall()
    RMB_code = '\xef\xbf\xa5'
    RMB_code = RMB_code.decode("utf8")
    tupletodic = { "data" : [[x[0], x[1], RMB_code + str(x[2]), RMB_code + str(x[3]), RMB_code + str(x[4]), RMB_code + str(x[5]), x[6], x[7], x[8]] for x in results] }
    return jsonify(tupletodic)
    
@app.route("/mysqltojson6")
def mysqltojson6():
    c = mysql.connect().cursor()
    c.execute("SELECT * FROM cal_int_eps")
    results = c.fetchall()
    RMB_code = '\xef\xbf\xa5'
    RMB_code = RMB_code.decode("utf8")
    tupletodic = { "data" : [[x[0], x[1], RMB_code + str(x[2]), RMB_code + str(x[3]), RMB_code + str(x[4]), RMB_code + str(x[5]), str('{0:.3g}'.format(x[6]*100)) + '%', str('{0:.3g}'.format(x[7]*100)) + '%',str('{0:.3g}'.format(x[8]*100)) + '%', str('{0:.3g}'.format(x[9]*100)) + '%', str('{0:.3g}'.format(x[10]*100)) + '%', x[11], x[12], RMB_code + str(x[13])] for x in results] }
    return jsonify(tupletodic)

@app.route("/multi_tab")
def multi_tab():
    return render_template("multi_tab.html")
    
@app.route("/menu")
def menu():
#For testing menu drop down bar
    return render_template("menu.html")

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404
    
if __name__ == "__main__":
    app.secret_key = '\x10\x1a^\xdf\xb8R}z\xce\xb4\x83\xb9b\x13\xd3]\x9a\x11\x12\x17\xb6\x05\xaf\xdb'
    app.debug = True
    
    #logging
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    #mysql
    #mysql = MySQL()
    #app.config.from_object('settings')
    #mysql.init_app(app)
    
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(app.config['HTTP_PORT']))
    
    
