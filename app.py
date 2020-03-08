from flask import Flask ,jsonify, request, make_response
import jwt
import datetime
from functools import wraps
import pyrebase
config = {
  "apiKey": "AIzaSyCxyhCnLdZ4Ol_WkUwtBVXhHGEP2j-hPcY",
  "authDomain": "buy-and-selling-7137d.firebaseapp.com",
  "databaseURL": "https://buy-and-selling-7137d.firebaseio.com",
  "projectId": "buy-and-selling-7137d",
  "storageBucket": "buy-and-selling-7137d.appspot.com",
  "messagingSenderId": "246130623636",
  "appId": "1:246130623636:web:c2a35f4127a12e38542081",
  "measurementId": "G-6JZXXTCN8R"
}


app=Flask(__name__)
l=[]
app.config['SECRET_KEY']='thisissecretkey'
firebase = pyrebase.initialize_app(config)#to connect with firebase
db = firebase.database()#to connect with firebase database
data=db.get()#to get the data from database
for user in data.each():
    l.append(user.key())
    l.append(user.val())
   
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
