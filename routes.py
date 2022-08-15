from app import app
from flask import render_template, request, session, redirect
from controllers import categories as categories_controller
from controllers import products as products_controller
from controllers import users as users_controller

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route("/register/", methods=['GET', 'POST'])
def register():
    return users_controller.register()

@app.route("/login/", methods=['GET', 'POST'])
def login():
    return users_controller.login()

@app.route("/logout/", methods=['GET'])
def logout():
    return users_controller.logout()

@app.route("/categories/", methods=['GET'])
def category_index():
    if 'email' in session:
        return categories_controller.index()
    else:
        return redirect("/login/")

@app.route("/categories/add/", methods=['GET', 'POST'])
def category_add():
    if 'email' in session:
        if request.method == 'GET':
            return categories_controller.add()
        elif request.method == 'POST':
            return categories_controller.store()
    else:
        return redirect("/login/")

@app.route("/categories/edit/<int:id>/", methods=['GET', 'POST'])
def category_edit(id):
    if 'email' in session:
        if request.method == 'GET':
            return categories_controller.edit(id)
        elif request.method == 'POST':
            return categories_controller.update(id)
    else:
        return redirect("/login/")

@app.route("/categories/delete/", methods=['POST'])
def category_delete():
    if 'email' in session:
        if request.method == 'POST':
            return categories_controller.destroy()
    else:
        return redirect("/login/")

@app.route("/products/", methods=['GET'])
def product_index():
    if 'email' in session:
        return products_controller.index()
    else:
        return redirect("/login/")

@app.route("/products/add/", methods=['GET', 'POST'])
def product_add():
    if 'email' in session:
        if request.method == 'GET':
            return products_controller.add()
        elif request.method == 'POST':
            return products_controller.store()
    else:
        return redirect("/login/")

@app.route("/products/edit/<string:slug>/", methods=['GET', 'POST'])
def product_edit(slug):
    if 'email' in session:
        if request.method == 'GET':
            return products_controller.edit(slug)
        elif request.method == 'POST':
            return products_controller.update(slug)
    else:
        return redirect("/login/")

@app.route("/products/delete/", methods=['POST'])
def product_delete():
    if 'email' in session:
        if request.method == 'POST':
            return products_controller.destroy()
    else:
        return redirect("/login/")

@app.route("/error/", methods=['GET'])
def error():
    error = request.args.get("error")
    return render_template("error.html", error=error)