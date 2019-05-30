from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
local_server=True


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
db = SQLAlchemy(app)


class Contacts(db.Model):
    '''
    sno, name phone_num, msg, date, email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)



@app.route("/")
def home():
    return render_template('index.html',params=params)

class Uploads(db.Model):

    sno = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(20), nullable=False)

@app.route("/post/",methods=['GET'])
def post():
    up=Uploads.query.filter_by().all()
    return render_template('post.html',params=params,posts=up)

@app.route("/about")
def about():
    return render_template('about.html',params=params)


@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone_num')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email )
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html',params=params)


app.run(debug=True)
