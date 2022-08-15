from connection import connection
from flask import render_template, redirect, request

def index():
    try:
        connect = connection()
        cursor = connect.cursor()

        query = "SELECT * FROM categories"
        cursor.execute(query)
        row = [x[0] for x in cursor.description]
        result = cursor.fetchall()
        
        categories = []
        for item in result:
            data = {
                "id": item[0],
                "code": item[1],
                "name": item[2],
                "description": item[3]
            }
            categories.append(data)

        return render_template("categories/index.html", categories=categories)
    except Exception as e:
        return redirect("/error?error=" + str(e))

def add():
    try:
        return render_template("categories/add.html")
    except Exception as e:
        return redirect("/error?error=" + str(e))

def store():
    try:
        code = request.form.get('code')
        name = request.form.get('name')
        description = request.form.get('description')

        connect = connection()
        cursor = connect.cursor()

        query = "INSERT INTO categories (code, name, description) VALUES (%s, %s, %s)"
        values = (code, name, description)
        cursor.execute(query, values)
        connect.commit()

        return redirect("/categories/")
    except Exception as e:
        return redirect("/error?error=" + str(e))

def edit(id):
    try:
        connect = connection()
        cursor = connect.cursor()

        query = "SELECT * FROM categories WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)

        row = [x[0] for x in cursor.description]
        result = cursor.fetchall()

        category = {
            "id": result[0][0],
            "code": result[0][1],
            "name": result[0][2],
            "description": result[0][3]
        }
        
        return render_template("categories/edit.html", category=category)
    except Exception as e:
        return redirect("/error?error=" + str(e))

def update(id):
    try:
        code = request.form.get('code')
        name = request.form.get('name')
        description = request.form.get('description')

        connect = connection()
        cursor = connect.cursor()

        query = "UPDATE categories SET code = %s, name = %s, description = %s WHERE id = %s"
        values = (code, name, description, id)
        cursor.execute(query, values)
        connect.commit()

        return redirect("/categories/")
    except Exception as e:
        return redirect("/error?error=" + str(e))

def destroy():
    try:
        id = request.form.get('id')

        connect = connection()
        cursor = connect.cursor()

        query = "DELETE FROM categories WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)
        connect.commit()

        return redirect("/categories/")
    except Exception as e:
        return redirect("/error?error=" + str(e))