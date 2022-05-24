from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dataclasses import dataclass
from flask_migrate import Migrate
import requests
from .producer import publish

from sqlalchemy import UniqueConstraint


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
app.config["SQLALCHEMY_DATABASE_URI"]="mysql://root:root@db/main"
CORS(app)

db=SQLAlchemy(app)

migrate = Migrate()
migrate.init_app(app, db)

@dataclass
class Product(db.Model):
    id:int
    title:str
    image:str

    id=db.Column(db.Integer,primary_key=True, autoincrement=False)
    title=db.Column(db.String(200))
    image=db.Column(db.String(200))

@dataclass
class ProductUser(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer)
    product_id=db.Column(db.Integer)

    UniqueConstraint("user_id","product_id",name="user_product.unique")



@app.route("/api/products")
def index():
    print(Product.query.all())
    return jsonify(Product.query.all())

@app.route("/api/products/<int:id>/like",methods=["POST"])
def like(id):
    req = requests.get("http://docker.for.mac.localhost:8000/api/user")
    json= req.json()
    try:
        productUser=ProductUser(user_id=json["id"],product_id=id)
        db.session.add(productUser)
        db.session.commit()
        publish("Product liked",id)

    except:
        abort(400,"You already liked this product")

    return jsonify(req.json())

if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")