from flask import Flask,request,render_template,session,redirect,url_for
import pymongo
from datetime import timedelta
import json

with open("mongoDB.json") as Json:
    user_doc = json.loads(Json.read())

mongo_url = 'mongodb+srv://' + user_doc["MongoID"]+ ':' + user_doc['MongoPassword']+ user_doc["MongoURL"]
client = pymongo.MongoClient(mongo_url)
db = pymongo.database.Database(client,'Cluster0')
Collect = pymongo.collection.Collection(db,'Collect')

app = Flask(__name__)
app.secret_key="juuuuwon"
    

@app.route('/register',methods=['GET','POST'])
def register():
  
          if not 'userEmail' in session:
              return redirect(url_for('signin'))
          return render_template('register.html')
   
@app.route('/books',methods=['GET','POST'])
def books():  

   if request.method =='GET':
       book = Collect.find()
       return render_template('books.html', result=book)

   if request.method =='POST':
       Collect.insert_one(request.form.to_dict(flat='true'))
       book = Collect.find()
       return render_template('books.html', result= book)


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        if not 'userEmail' in session:
            return render_template('signup.html')
       

        return render_template('welcome.html',info=session['userEmail'])

    elif request.method == 'POST':
        if not 'userEmail' in session:
              
            Collect.insert_one(request.form.to_dict(flat='true'))
            session['userEmail']=request.form['userEmail'] 
            return render_template('welcome.html',info=session['userEmail'])
        return render_template('welcome.html',info=session['userEmail'])


@app.route('/signin', methods=['GET','POST'])
def signin():
    if  request.method == 'GET':
        if not 'userEmail' in session:
            return render_template('signin.html')
        return render_template('welcome.html',info=session['userEmail'])

    elif request.method == 'POST':
        if 'userEmail' in session:
            return render_template('welcome.html',info=session['userEmail'])
        if Collect.find_one(request.form.to_dict(flat='true')) is not None:
            session['userEmail'] = request.form['userEmail']
            return redirect(url_for('register'))
        return redirect(url_for('signin')) 
@app.route('/logout')
def logout():
    if session['userEmail']:
       session.pop('userEmail')
       return redirect(url_for('signin'))
    return redirect(url_for('signin'))

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=60)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5010)
