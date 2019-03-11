from flask import Flask, session, render_template, request, redirect, g, url_for, Response
from jinja2 import Template
import os, pymysql
import time

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

# config
conn = pymysql.connect(host="localhost", user="root", password="", db="blog")
cur = conn.cursor()

def validate_user(user, password):
    cur.execute("SELECT * FROM `user` where (`username`='{0}') and (`password`='{1}');".format(user, password))
    cx = cur.fetchall()
    if(len(cx) == 1):
        return True
    else:
        return False
    
def mod_replace(word,dictrep):
    for key,val in dictrep.items():
        word = word.replace(key, val)
    return word

# APP
app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'user' in session:
        return redirect(url_for('protected'))

    if request.method == 'POST':
        session.pop('user', None)
        # DB SCHECK
        if validate_user(request.form['username'], request.form['password']) == True:
            session['user'] = request.form['username']
            session['logintime'] = time.time() * 1000;
            return redirect(url_for('protected'))

    return render_template('/login.html', title="ECHOBOTS")

@app.route('/protected')
def protected():
    if g.user:
        return mod_replace(render_template('home.html'), {'{ini_user}': session['user'], '{login_time_12}': str(session['logintime'])})

    return redirect(url_for('login'))

@app.route('/user-now', methods=['GET', 'POST'])
def usernow():
    # template883 =open('templates/protected.html','r').read()
    # template883 = template883.replace('{0}', session['user'])
    # return template883;
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		cur.execute("INSERT INTO `data` (title, body) VALUES ('{0}', '{1}')".format(title, body))
		conn.commit()
		return redirect(url_for('index'))
	else:
		return render_template("home.html", title='dashboard')

@app.route("/news")
def news():
	cur.execute("SELECT * FROM `data`")
	data = cur.fetchall()
	return render_template("news.html", data=data, title="data")

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
	app.run(debug=True)
	# app.run(host=0.0.0.0, port=5000)