from logging import debug
from flask import Flask, render_template, jsonify, request
import flask
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__)

app.secret_key = "hasib"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'data_crawler'
app.config['MYSQL_CURSORClASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('./templates/searchclusters.html')

@app.route("/posturl",methods=["POST","GET"])
def posturl():
    cursor = mysql.connection.cursor()
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        urls = request.form.getlist('urls[]')
        for value in urls:
            cur.execute("INSERT INTO checkdata (test_url) VALUES (%s)", [value])
            mysql.connection.commit()
        cur.close()
        msg = 'Urls added successfully!'
    return jsonify(msg)

if __name__ == "__main__":
    app.run(debug=True)