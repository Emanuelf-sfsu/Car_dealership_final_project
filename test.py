from peewee import *
from flask import Flask,jsonify,request
import json

#Init app
app = Flask(__name__)
database = SqliteDatabase('SFAutoMall.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Manufacturer(BaseModel):
    m_name = TextField(column_name='M_Name', primary_key=True)
    phone = IntegerField(column_name='Phone', null=True)
    state = TextField(column_name='State', null=True)

    class Meta:
        table_name = 'Manufacturer'

class Offices(BaseModel):
    district_id = AutoField(column_name='District_id')
    phone = IntegerField(column_name='Phone', null=True)
    state = TextField(column_name='State')

    class Meta:
        table_name = 'Offices'

class Person(BaseModel):
    age = IntegerField(column_name='Age', null=True)
    license = IntegerField(column_name='License')
    p_name = TextField(column_name='P_Name', primary_key=True)

    class Meta:
        table_name = 'Person'
        indexes = (
            (('p_name', 'license'), False),
        )

class Vehicle(BaseModel):
    buyer = ForeignKeyField(column_name='Buyer', constraints=[SQL("DEFAULT 'NA'")], field='p_name', model=Person, null=True)
    district = ForeignKeyField(column_name='District_Id', constraints=[SQL("DEFAULT 0")], model=Offices)
    make = ForeignKeyField(column_name='Make', field='m_name', model=Manufacturer)
    model = TextField(column_name='Model', primary_key=True)
    repair = IntegerField(column_name='Repair', null=True)
    value = IntegerField(column_name='Value', null=True)
    year = IntegerField(column_name='Year', null=True)

    class Meta:
        table_name = 'Vehicle'
        indexes = (
            (('make', 'model'), False),
            (('make', 'value'), False),
        )

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False


# get all offices
@app.route('/offices',methods=['GET'])
def get_Offices():
    query = Offices.select()
    data =[]
    for look in query:
        result = {"District_id":look.district_id,"phone":look.phone,"State":look.state}
        data.insert(len(data),result)
    print(data)
    return json.dumps(data,indent = 6)

# get all vehicle
@app.route('/vehicle',methods=['GET'])
def get_Vehicle():
    query = Vehicle.select()
    data =[]
    for look in query:
        result = {
                    "make":look.make.m_name,
                    "model":look.model,
                    "year":look.year,
                    "value":look.value,
                    "buyer":look.buyer.p_name,
                    "repair":look.repair,
                    "District_id":look.district.district_id,
                }
        data.insert(len(data),result)
    print(data[1])
    return json.dumps(data,indent = 6)

#Run Server
if __name__ == '__main__':
    app.run(debug=True)