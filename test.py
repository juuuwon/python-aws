
from flask import Flask, render_template,request,jsonify
import pymongo
app = Flask(__name__)


mongo_url = 'mongodb+srv://juuuwon:kim-03rla@cluster0-pjygz.mongodb.net/test?retryWrites=true'
client = pymongo.MongoClient(mongo_url)
db = pymongo.database.Database(client,'Cluster0')
Collect = pymongo.collection.Collection(db,'Collect')


@app.route('/register')
def register():
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





if __name__=='__main__':
	app.run(host='0.0.0.0', port=5010)
