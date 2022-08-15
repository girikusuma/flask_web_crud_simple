import re
from connection import connection
from flask import render_template, redirect, request

def index():
    try:
        connect = connection()
        cursor = connect.cursor()

        query = "SELECT * FROM products"
        cursor.execute(query)
        row = [x[0] for x in cursor.description]
        result = cursor.fetchall()
        
        products = []
        for item in result:
            q = "SELECT * FROM categories WHERE id = %s"
            v = (item[1],)
            cursor.execute(q, v)
            row = [x[0] for x in cursor.description]
            category = cursor.fetchall()
            data = {
                "id": item[0],
                "category": category[0][2],
                "code": item[2],
                "name": item[3],
                "slug": item[4],
                "description": item[5],
                "price": item[6],
                "stock": item[7]
            }
            products.append(data)

        return render_template("products/index.html", products=products)
    except Exception as e:
        return redirect("/error?error=" + str(e))

def add():
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
                "name": item[2],
            }
            categories.append(data)
        
        return render_template("products/add.html", categories=categories)
    except Exception as e:
        return redirect("/error?error=" + str(e))

def store():
    try:
        code = request.form.get('code')
        category_id = request.form.get('category_id')
        name = request.form.get('name')
        slug = slugify(name)
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')

        connect = connection()
        cursor = connect.cursor()

        query = "INSERT INTO products (code, category_id, name, slug, description, price, stock) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (code, category_id, name, slug, description, price, stock)
        cursor.execute(query, values)
        connect.commit()

        return redirect("/products/")
    except Exception as e:
        return redirect("/error?error=" + str(e))

def edit(slug):
    try:
        connect = connection()
        cursor = connect.cursor()

        query = "SELECT * FROM products WHERE slug = %s"
        values = (slug,)
        cursor.execute(query, values)
        row = [x[0] for x in cursor.description]
        result = cursor.fetchall()
        
        product = {
            "id": result[0][0],
            "category_id": result[0][1],
            "code": result[0][2],
            "name": result[0][3],
            "slug": result[0][4],
            "description": result[0][5],
            "price": result[0][6],
            "stock": result[0][7]
        }

        q = "SELECT * FROM categories"
        cursor.execute(q)
        row = [x[0] for x in cursor.description]
        result = cursor.fetchall()
        
        categories = []
        for item in result:
            data = {
                "id": item[0],
                "name": item[2],
            }
            categories.append(data)
        
        return render_template("products/edit.html", product=product, categories=categories)
    except Exception as e:
        return redirect("/error?error=" + str(e))

def update(slug):
    try:
        code = request.form.get('code')
        category_id = request.form.get('category_id')
        name = request.form.get('name')
        slug_new = slugify(name)
        description = request.form.get('description')
        price = request.form.get('price')
        stock = request.form.get('stock')

        connect = connection()
        cursor = connect.cursor()

        query = "UPDATE products SET code = %s, category_id = %s, name = %s, slug = %s, description = %s, price = %s, stock = %s WHERE slug = %s"
        values = (code, category_id, name, slug_new, description, price, stock, slug)
        cursor.execute(query, values)
        connect.commit()

        return redirect("/products/")
    except Exception as e:
        return redirect("/error?error=" + str(e))

def destroy():
    try:
        id = request.form.get('id')

        connect = connection()
        cursor = connect.cursor()

        query = "DELETE FROM products WHERE id = %s"
        values = (id,)
        cursor.execute(query, values)
        connect.commit()

        return redirect("/products/")
    except Exception as e:
        return redirect("/error?error=" + str(e))

def slugify(value):
    slug = re.sub(r"(\"|\[|\])", "", value)
    slug = slug.strip().lower()
    slug = re.sub(r"(\s+|_)", "-", slug)

    return slug