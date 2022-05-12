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
#                After creating Manufacturer(s)Schema run: 
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

from math import prod
from pydoc import describe
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os 
from dotenv import load_dotenv

#Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'SFAutoMall.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Init Marshmallow
ma = Marshmallow(app)

# Manufacturer/class, find more at Flask-marshmellow
class Manufacturer(db.Model):
    M_Name = db.Column(db.String(100) ,primary_key = True,unique=True)
    Phone = db.Column(db.Integer)
    State = db.Column(db.String(100))

    def __init__(self, M_Name, Phone, State):
        self.M_Name = M_Name
        self.Phone = Phone
        self.State = State


# Manufacturer Schema 
class ManufacturerSchema(ma.Schema):
    class Meta:
        fields = ( 'M_Name', 'Phone', 'State')
#Init Schema
#`strict = True` removes warning from console. 
# Manufacturer_schema is for singlar entry and Manufacturers is for multiple 
# used commands 
Manufacturer_schema = ManufacturerSchema() 
Manufacturers_schema = ManufacturerSchema(many=True) 

# Offices
class Offices(db.Model):
    District_id = db.Column(db.Integer ,primary_key = True,unique=True)
    Phone = db.Column(db.Integer)
    State = db.Column(db.String(100))

    def __init__(self,District_id, Phone, State):
        self.District_id = District_id
        self.Phone = Phone
        self.State = State


# Offices Schema 
class OfficesSchema(ma.Schema):
    class Meta:
        fields = ( 'District_id', 'Phone', 'State')


# Office
Office_schema = OfficesSchema() 
Offices_schema = OfficesSchema(many=True)

# Vehicles--------------------------
class Vehicle(db.Model):
    Model = db.Column(db.String(100),primary_key = True)
    Year = db.Column(db.Integer)
    Value = db.Column(db.Integer)
    Repair = db.Column(db.Integer)
    child = db.relationship('child',backref='Vehicle')

class child(db.Model):
    Buyer = db.Column(db.String(100),db.ForeignKey('Vehicle.Model'))
    Make = db.Column(db.String(100),db.ForeignKey('Vehicle.Model'))
    District_id = db.Column(db.Integer,db.ForeignKey('Vehicle.Model'))

    def __init__(self,Make, Model, Year,Value,Buyer,Repair,District_id):
        self.District_id = District_id
        self.Make = Make
        self.Model = Model
        self.Year = Year
        self.Value = Value
        self.Buyer = Buyer
        self.Repair = Repair




# Vehicle Schema 
class VehicleSchema(ma.Schema):
    class Meta:
        fields = ( 'Make', 'Model', 'Year','Value','Buyer','Repair','District_id')


# Vehicle
Vehicle_schema = VehicleSchema() 
Vehicles_schema = VehicleSchema(many=True)
# ----------------------------------------------
# #Create Manufacturer
# @app.route('/Manufacturer',methods=['POST'])
# def add_Manufacturer():
#     name = request.json['name']
#     description = request.json['description']
#     price = request.json['price']
#     qty = request.json['qty']

#     # Creating new Manufacturer object
#     new_Manufacturer = Manufacturer(name,description,price,qty)
#     # adding new entry to data base
#     db.session.add(new_Manufacturer)
#     db.session.commit()

#     return Manufacturer_schema.jsonify(new_Manufacturer)

# get all Manufacturers
@app.route('/Manufacturer',methods=['GET'])
def get_Manufacturers():
    all_Manufacturers = Manufacturer.query.all()
    result = Manufacturers_schema.dump(all_Manufacturers)
    return jsonify(result)

# get all offices
@app.route('/offices',methods=['GET'])
def get_Offices():
    all_Offices = Offices.query.all()
    result = Offices_schema.dump(all_Offices)
    return jsonify(result)

# get all Vehicle
@app.route('/vehicle',methods=['GET'])
def get_Vehicle():
    all_Vehicle = Vehicle.query.all()
    result = Vehicle_schema.dump(all_Vehicle)
    return jsonify(result)



#get single
@app.route('/Manufacturer/<id>',methods=['GET'])
def get_Manufacturer(id):
    Manufacturer = Manufacturer.query.get(id)
    return Manufacturer_schema.jsonify(Manufacturer)

# #Update Manufacturer
# @app.route('/Manufacturer/<id>',methods=['PUT'])
# def update_Manufacturer():
#     Manufacturer = Manufacturer.query.get(id)

#     #getting data from the body
#     name = request.json['name']
#     description = request.json['description']
#     price = request.json['price']
#     qty = request.json['qty']

#     Manufacturer.name = name
#     Manufacturer.description = description
#     Manufacturer.price = price
#     Manufacturer.qty = qty

#     db.session.commit()


#     return Manufacturer_schema.jsonify(Manufacturer)

# #Delete
# @app.route('/Manufacturer/<id>',methods=['DELETE'])
# def delete_Manufacturer(id):
#     Manufacturer = Manufacturer.query.get(id)
#     db.session.delete(Manufacturer)
#     db.session.commit()
#     return Manufacturer_schema.jsonify(Manufacturer)





# Test
# @app.route('/',methods=['GET'])
# def get():
#         return jsonify({'msg':'Hello world'})

#Run Server
if __name__ == '__main__':
    app.run(debug=True)