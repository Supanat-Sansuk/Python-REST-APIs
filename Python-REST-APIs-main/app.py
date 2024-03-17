from flask import Flask, request, render_template, redirect, jsonify
import os
import mysql.connector as mysql

app = Flask(__name__)

conn = mysql.connect(
    host="localhost",
    user="root",
    password="Boat2547",
    port=3306,
    database="my_memo"
)

@app.route('/', methods=["GET"])
def index():
    cur = conn.reconnect()

    cur = conn.cursor() 
    sql = "SELECT idmemo, firstname, lastname, email FROM memo"
    cur.execute(sql)
    names = cur.fetchall() 
    cur.close()  
    return render_template('index.html', names=names)

@app.route('/product', methods=["GET"])
def product():
    item = {
        'Name': "Adidas",
        'Model': 'Ultra Boost',
        'Price': 180.00
    }
    return (item)

@app.route('/news/<id>', methods=["GET"])
def news(id):
    return "Topic no. is " + id

@app.route('/profile', methods=["GET"])
def profile():
    name = request.args.get("name")
    age = request.args.get("age")
    email = request.args.get("email")
    return f"<b>I am {name}, {age} years old. This is my email: {email}</b>"

@app.route('/post-data', methods=["POST"])
def post_data():
    name = request.form.get("name")
    age = request.form.get("age")
    email = request.form.get("email")
    return f"<b>I am {name}, {age} years old. This is my email: {email}</b>"

@app.route('/adduser', methods=["GET"])
def add_newuser():
    return render_template('add_user.html')

@app.route('/adduser_todb', methods=["POST"])
def adduser_todb():
    cur = conn.reconnect()

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')

    sql = "INSERT INTO my_memo.memo (firstname, lastname, email) VALUES (%s, %s, %s)"
    data = (firstname, lastname, email)

    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit() 
    conn.close()
    return redirect('/')
    

@app.route('/delete/<idmemo>', methods=["GET"])
def delete(idmemo):
    cur = conn.reconnect()
    sql = "DELETE FROM memo WHERE idmemo=%s"
    data = (idmemo,) 
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    cur.close()
    return redirect('/')

@app.route('/edit/<idmemo>', methods=["GET"])
def edit(idmemo):
    cur = conn.reconnect()
    cur = conn.cursor()  
    sql = "SELECT idmemo, firstname, lastname, email "
    sql += "FROM memo WHERE idmemo=%s"
    data = (idmemo,)
    cur.execute(sql, data)
    name = cur.fetchone() 
    conn.close()
    return render_template("edit_user.html", name=name)

@app.route('/edituser_todb', methods=["POST"])
def edituser_todb():
    cur.conn.reconnect()

    idmemo = request.form.get('idmemo')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')

    sql = "UPDATE memo SET firstname=%s, lastname=%s, email=%s "
    sql += "WHERE idmemo=%s"
    data = (firstname, lastname, email, idmemo)
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/getuser/v1/<idmemo>', methods=["GET"])
def get_user_by_id(idmemo):
    cur = conn.reconnect()
    cur = conn.cursor()

    sql = "SELECT idmemo, firstname, lastname, email "
    sql += "FROM memo WHERE idmemo=%s ORDER BY firstname"
    data = (idmemo,)
    cur.execute(sql, data)
    records = cur.fetchall()
    cur.close()
    return jsonify(records)

@app.route('/getuser', methods=["GET"])
def get_all_users():
    cur = conn.reconnect()
    cur = conn.cursor()

    sql = "SELECT idmemo, firstname, lastname, email FROM memo ORDER BY firstname"
    cur.execute(sql)
    records = cur.fetchall()
    cur.close()
    return jsonify(records)

@app.route('/postuser', methods=["POST"])
def post_user():
    response = request.get_json()
    firstname = response.get('firstname')
    lastname = response.get('lastname')
    email = response.get('email')

    cur = conn.cursor()
    sql = "INSERT INTO memo(firstname, lastname, email) VALUES (%s, %s, %s)"
    data = (firstname, lastname, email)
    cur.execute(sql, data)
    conn.commit()
    cur.close()
    return redirect('/getuser/v1/1')

@app.route('/delete/<email>', methods=["DELETE"])
def delete_user(email):
    cur = conn.reconnect()
    cur = conn.cursor()
    sql = "DELETE FROM memo WHERE email=%s"
    data = (email,)
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return redirect('/getuser')

@app.route('/put_user', methods=['PUT'])
def put_user():
    response = request.get_json()

    idmemo = response['idmemo']
    firstname = response['firstname']
    lastname = response['lastname']
    email = response['email']

    conn.reconnect()
    cur = conn.cursor()
    sql = "UPDATE memo SET firstname=%s, lastname=%s, email=%s WHERE idmemo=%s"
    data = (firstname, lastname, email, idmemo)
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return redirect('/getuser')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)