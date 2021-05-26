#basic mandatory syntax for flask app
#@import:
# @app: set app variable to flask app
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
app= Flask(__name__)
#basic mandatory syntax for flask-sqlalchemy
# @import:
# @app.config: basic mandatory config for sqlite db app, see do
# @db: set db variable to SQLAlchemy App

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

#class definition
#defines the db
# @attributes: my columns
# @__repr__ : default object representation method
class Company(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column('Name',db.String(50), unique=True, nullable=False)
    legalEntity= db.Column('Legal Entity', db.String(50))
    employees= db.Column('Employees', db.Integer)
    equity= db.Column('Equity',db.Integer)

    #overwrite with formatted(parameterized) String for terminal representation
    def __repr__(self):
        return f"Name: {self.name} \nLegal Entity: {self.legalEntity} \nEmployees: {self.employees} \nEquity: {self.equity} \n"


routelist = ['/','/companies','companies/<id>']


#Start without functionality
@app.route('/')
def index():
    return 'Python Test API 1.0'


#get all companies
@app.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    #make it json compatible
    companieslist = []
    for company in companies:
        company_data = {'name': company.name, 'Legal Entity': company.legalEntity, 'Employees': company.employees, 'Equity': company.equity, 'ID': company.id}
        companieslist.append(company_data)

    return {'Companies': companieslist}


#get company by id
@app.route('/companies/<id>', methods=['GET'])
def get_companyById(id):
    company = Company.query.get(id)
    if company is None:
        return "Desired ID could not be found /GET cancelled"
    #dictionaries are serializable by design, else try 'jsonify(<your data>)
    return {'name': company.name, 'Legal Entity': company.legalEntity, 'Employees': company.employees, 'Equity': company.equity, 'ID': company.id}


#delete company by id
@app.route('/companies/<id>', methods=['DELETE'])
def delete_company(id):
    company = Company.query.get_or_404(id)
    if company is None:
    	return "Desired ID could not be found /DELETE cancelled"
    db.session.delete(company)
    db.session.commit()
    return {'name': company.name, 'Legal Entity': company.legalEntity, 'Employees': company.employees, 'Equity': company.equity, 'ID': company.id}


#add company
@app.route('/companies', methods=['POST'])
def add_company():
    company= Company(name=request.json['name'], legalEntity=request.json['legalEntity'],employees=request.json['employees'],equity=request.json['equity'])
    companies = Company.query.all()
    for comp in companies:
        if comp.name == company.name:
            return f"{company.name} is already in db! /POST cancelled"
    db.session.add(company)
    db.session.commit()
    return {'name': company.name, 'Legal Entity': company.legalEntity, 'Employees': company.employees, 'Equity': company.equity, 'ID': company.id}

