from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

import certifi

client = MongoClient("mongodb+srv://basitabass27411:iamahacker313@baiq.o4c0pn6.mongodb.net/?retryWrites=true&w=majority" ,tlsCAFile = certifi.where())

db = client['my_notes_database']
coll = db['my_notes_table']
# coll.insert_one({'test':'test1'})  

app = Flask(__name__)

@app.route('/')
def home():
     notes = list(coll.find({})) 
     
     return render_template("home.html", homeIsActive = True, addNoteIsActive = False, notes = notes)

@app.route('/add-note', methods=['GET', 'POST'])
def addNote():
     if request.method == 'GET':
         return render_template("addNote.html", homeIsActive = False, addNoteActive = True)
     elif request.method == 'POST':
          id = request.form['id']
          title = request.form['title']
          description = request.form['description']
          coll.insert_one({'title': title, 'description': description, 'id': id})
          return redirect('/')
@app.route('/edit-note', methods = ['GET', 'POST'])
def editNote():
     if request.method == 'GET':
          noteId = request.args.get('form')
          note = dict(coll.find_one({"_id": ObjectId(noteId)})) 
          return render_template("editNote.html", note = note)  
     elif request.method == 'POST':
          noteId = request.form['_id']
          title = request.form['title']
          description = request.form['description']   
          
          coll.update_one({'_id': ObjectId(noteId)}, {'$set': {'title': title, 'description': description}})
          return redirect('/')
          
@app.route('/delete-note', methods = ['POST']) 
def deleteNote():
     noteId = request.form['_id']
     coll.delete_one({'_id': ObjectId(noteId)})
     return redirect('/') 

if __name__ == "__main__":
     app.run(debug=True)