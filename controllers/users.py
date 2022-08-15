from connection import connection
from flask import render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

def register():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')

            connect = connection()
            cursor = connect.cursor()

            q = "SELECT * FROM users WHERE username = %s"
            v = (username,)
            cursor.execute(q, v)
            row = [x[0] for x in cursor.description]
            result = cursor.fetchone()

            print(result)

            if not result == None:
                flash("Username already exists")
                return redirect("/register/")
            
            query = "INSERT INTO users (username, password, first_name, last_name, email) VALUES (%s, %s, %s, %s, %s)"
            values = (username, generate_password_hash(password), first_name, last_name, email)
            cursor.execute(query, values)
            connect.commit()

            return redirect("/login/")
        else:
            return render_template("users/register.html")
    except Exception as e:
        return redirect("/error?error=" + str(e))

def login():
    try:
        if request.method == 'POST':
            user = request.form.get('user')
            password = request.form.get('password')

            connect = connection()
            cursor = connect.cursor()

            q = "SELECT * FROM users WHERE username = %s OR email = %s"
            v = (user, user)
            cursor.execute(q, v)
            row = [x[0] for x in cursor.description]
            result = cursor.fetchone()

            if not check_password_hash(result[2], password):
                flash("Password not match")
                return redirect("/login/")

            session['username'] = result[1]
            session['email'] = result[5]

            return redirect("/")
        else:
            return render_template("users/login.html")
    except Exception as e:
        return redirect("/error?error=" + str(e))

def logout():
    try:
        session.clear()
        return redirect("/login/")
    except Exception as e:
        return redirect("/error?error=" + str(e))