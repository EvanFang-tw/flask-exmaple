from crypt import methods
from flask import Flask, jsonify, redirect, render_template, abort, request, url_for
from db import db
from Product import Product

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:adminpw@db:5432/mydb"
db.init_app(app)

# Example: return string
@app.route("/")
def index():
    return "<h1>Flask is cool</h1>"


# Example: use template
@app.route("/hello")
def hello():
    return render_template("hello.html", message="world")


# Example: post form and redirect
@app.route("/form", methods=["GET", "POST"])
def get_form():
    if request.method == "POST":
        username = request.form["username"]
        return redirect(url_for("greeting", username=username))
    else:
        return render_template("form.html")


@app.route("/sayhi/<username>")
def greeting(username):
    return f"<h1>Hi {username}</h1>"


# Example: return 404
@app.route("/404")
def not_found():
    abort(404)
    # or use return with message:
    # return "Oops! Not Found.", 404


# Example: return json list
@app.route("/api/list")
def get_list():
    data = [
        {
            "name": "David",
            "age": 18,
        },
        {
            "name": "Mary",
            "age": 61,
        },
    ]
    return jsonify(data)


# Example: get json into dict from request
@app.route("/api/data", methods=["POST"])
def create_data():
    app.logger.info(request.json)
    return "ok", 201


# Examples: interact with database
@app.route("/api/products")
def get_all_products():
    products = [p.json for p in Product.get_all()]
    return jsonify(products)
    # Example of using raw sql:
    # query_data = db.engine.execute("select * from products;")
    # products = [{"id": id, "name": name} for id, name in query_data]
    # return products


@app.route("/api/product", methods=["POST"])
def add_product():
    name = request.json["name"]
    product = Product(None, name)
    product.save()
    return jsonify(product.json), 201
