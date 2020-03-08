from flask import Flask ,jsonify, request, make_response
import jwt
import datetime
from functools import wraps
import sqlite3
import pyrebase
config = {
  "apiKey": "AIzaSyCPYEjH0XJzbMARg_mIlOqtMJa0QW1DgGQ",
  "authDomain": "fireapp-8a37a.firebaseapp.com",
  "databaseURL": "https://fireapp-8a37a.firebaseio.com",
  "projectId": "fireapp-8a37a",
  "storageBucket": "fireapp-8a37a.appspot.com",
  "messagingSenderId": "593560484305",
  "appId": "1:593560484305:web:8b2dc652f42921deeec8f0",
  "measurementId": "G-J38QTVJH3B"
}


app=Flask(__name__)
l=[]
app.config['SECRET_KEY']='thisissecretkey'
firebase = pyrebase.initialize_app(config)
db = firebase.database()
data=db.get()
for user in data.each():
    l.append(user.key())
    l.append(user.val())
    print(user.key()) # Morty
    print(user.val()) # {name": "Mortimer 'Morty' Smith"}
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token=request.args.get('token')
        if not token:
            return jsonify({'messege':'token is missing'}),403
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'messege':'invalide token'}),403     
        return f(*args, **kwargs)
    return decorated
    
 
@app.route('/unprotected')
def unprotected():
    return jsonify({'msg':'anyone can see this'})
    
@app.route('/protected')
@token_required
def protected():
    return jsonify({'msg':l})

@app.route('/login')
def login():
    auth=request.authorization
    if auth and auth.password == 'password':
        token=jwt.encode({'user':auth.username,'exp': datetime.datetime.utcnow() + datetime.timedelta(days=2) },app.config['SECRET_KEY'])
        
        return jsonify({'token':token.decode('UTF-8')})
 
        
    return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})

    

     
    
   # return make_response('Could not verify!', 401, {'WWW.-Authenticate' : 'Basic realm="Login Required"'})
     
if __name__=='__main__':
    app.run(debug=True)    
