from distutils.log import debug
import re
from urllib import request
from flask import Flask,redirect,url_for,render_template,request
import pymongo
from bson.objectid import ObjectId

app=Flask(__name__)
mongo=pymongo.MongoClient(host="localhost",port=27017)
db=mongo.codeapp

@app.route("/",methods=['GET','POST'])
def home():
    all_codes=db.codes.find()
    return render_template("home.html",codes=all_codes)

@app.route("/add-code",methods=['POST'])
def add_code():
    new_code=request.form.get('code')
    db.codes.insert_one({'text':new_code})
    return redirect(url_for('home'))

@app.route("/delete-code",methods=['POST'])
def delete_code():
    oid=request.form.get('delete')
    db.codes.delete_one({"_id":ObjectId(oid)})
    return redirect(url_for('home'))

@app.route("/edit-code",methods=['POST'])
def edit_code():
        oid=request.form.get('edit')
        code=dict(db.codes.find_one({"_id":ObjectId(oid)}))
        return render_template("edit.html",code=code)

@app.route("/update-code",methods=['POST'])
def update_code():
    oid=request.form.get('edited')
    edited_code=request.form.get('edited_code')
    db.codes.update_one({"_id":ObjectId(oid)},{"$set":{'text':edited_code}})
    return redirect(url_for('home'))
    
    
    
    
    
    

if __name__=="__main__":
    app.run(debug=True)