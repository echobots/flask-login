from flask import Flask, render_template, request, url_for, redirect
from jinja2 import Template
import pymysql

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")

# config
conn = pymysql.connect(host="localhost", user="root", password="", db="crud")
cur = conn.cursor()

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']
		cur.execute("INSERT INTO data (title, body) VALUES ('{0}', '{1}')".format(title, body))
		conn.commit()
		return redirect(url_for('index'))
	else:
		return render_template("home.html")

@app.route("/news")
def news():
	cur.execute("SELECT * FROM data")
	data = cur.fetchall()
	return render_template("news.html", data=data)

if __name__ == "__main__":
	app.run(debug=True)