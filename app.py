#=============================================================================
#   Assignment:  Car Dealship Extra Credit Assignment
#
#       Author:  Emanuel Francis
#     Language:  Python 3.8
#   To Compile:  EXPLAIN HOW TO COMPILE THIS PROGRAM
#
#        Class:  CSC 675
#   Instructor:  NAME OF YOUR COURSE'S INSTRUCTOR
#     Due Date:  DATE AND TIME THAT THIS PROGRAM IS/WAS DUE TO BE SUBMITTED
#
#+-----------------------------------------------------------------------------
#
#  Description:  This restapi will be used to communicate with the Mysql database
#                for the final project. There will be several endpoints that will
#                help achieve the frontends requests.
#                
#                Use `python3 app.py` to start the rest server. 
#                After creating product(s)Schema run: 
#                python
#                db.create_all()                
#
#        Input:  Recieves the endpoint http://localhost:5000/{endpoint here}
#
#       Output:  Returns a JSON file with the desired output
#
#   Known Bugs: N/A
#
#===========================================================================*/

from pydoc import describe
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# Product/class, find more at Flask-marshmellow
class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100),unique = True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

# Product Schema 
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')

#Init Schema
#`strict = True` removes warning from console. 
# product_schema is for singlar entry and products is for multiple 
# used commands 
product_schema = ProductSchema() 
products_schema = ProductSchema(many=True,) 

#Create Product
@app.route('/product',methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    # Creating new product object
    new_product = Product(name,description,price,qty)
    # adding new entry to data base
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

#get all products
@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

#get single
@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

#Update Product
@app.route('/product/<id>',methods=['PUT'])
def update_product():
    product = Product.query.get(id)

    #getting data from the body
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()


    return product_schema.jsonify(product)






# Test
# @app.route('/',methods=['GET'])
# def get():
#         return jsonify({'msg':'Hello world'})

#Run Server
if __name__ == '__main__':
    app.run(debug=True)