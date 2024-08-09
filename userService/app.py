from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import jwt
import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@user_db:5432/user_db')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mySuperSecretKey')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(10), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    type = data.get('type')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(name=name, username=username, password=hashed_password, type=type)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        payload = {
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'access_token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/test', methods=['GET'])
def test():
    return "This is a test!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
