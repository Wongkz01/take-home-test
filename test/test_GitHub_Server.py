import flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
import requests

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = '1234567890987654321'  # Set your secret key for JWT encryption

# Configure the database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TODO_list.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    github_access_token = db.Column(db.String(200))

    def __repr__(self):
        return '<User {0}>'.format(self.username)

# Define the TO-DO List model
class todoList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_ID = db.Column(db.String(100), nullable=False)
    num = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    date_Created = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<todoList {0}>'.format(self.title)

with app.app_context():
    db.create_all()

# JWT Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Start Up Page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Backend Software Engine Take Home Test</h1>
                <p>Python, REST API, Flask, SQLAlchemy</p>'''

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already exists!'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Invalid username or password!'}), 401

    user = User.query.filter_by(username=auth.username).first()

    if not user or not check_password_hash(user.password, auth.password):
        return jsonify({'message': 'Invalid username or password!'}), 401

    token = jwt.encode({'username': user.username}, app.config['SECRET_KEY'])

    return jsonify({'token': token}), 200

# GitHub Authentication Route
@app.route('/github/auth', methods=['GET'])
def github_auth():
    client_id = '86ac12c569295ae2d1bf'
    redirect_uri = 'http://localhost:5000/github/callback'
    github_auth_url = f'https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}'
    return redirect(github_auth_url)


# GitHub Authentication Callback Route
@app.route('/github/callback', methods=['GET'])
def github_callback():
    client_id = '86ac12c569295ae2d1bf'
    client_secret = 'ef04cb9927eab6d58bd35ea166cb1c393597f21c'
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    token_url = 'https://github.com/login/oauth/access_token'
    headers = {'Accept': 'application/json'}
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
    }
    response = requests.post(token_url, headers=headers, data=payload)

    if response.status_code == 200:
        access_token = response.json().get('access_token')

        # Use the access token to fetch the user's GitHub profile
        user_url = 'https://api.github.com/user'
        headers = {'Authorization': f'token {access_token}'}
        response = requests.get(user_url, headers=headers)

        if response.status_code == 200:
            github_username = response.json().get('login')
            user = User.query.filter_by(username=github_username).first()

            if user is None:
                # Register the user if they don't exist in the database
                new_user = User(username=github_username, github_access_token=access_token)
                db.session.add(new_user)
                db.session.commit()

            # Generate a JWT token for authentication
            token = jwt.encode({'username': github_username}, app.config['SECRET_KEY'])

            # Redirect back to the client application with the JWT token
            redirect_url = '<your-client-url>'
            return redirect(f'{redirect_url}?token={token}')

    # Redirect to an error page or handle the authentication failure
    return redirect('<error-url>')

# List All TO-DO items
@app.route('/todo/all', methods=['GET'])
@token_required
def todo_all(current_user):
    todo_list = todoList.query.filter_by(user_ID=current_user.username).all()
    results = []
    for todo in todo_list:
        results.append({
            'id': todo.id,
            'user_ID': todo.user_ID,
            'num': todo.num,
            'title': todo.title,
            'status': todo.status,
            'date_Created': todo.date_Created
        })

    return jsonify(results)

# Add a new TO-DO item
@app.route("/todo", methods=['POST'])
@token_required
def todo_insert(current_user):
    todo_data = request.get_json()
    todo = todoList(**todo_data)
    db.session.add(todo)
    db.session.commit()
    return jsonify("Server Success: TODO has been added.")

# Delete a TO-DO item
@app.route("/todo/<num>", methods=["DELETE"])
@token_required
def todo_delete(current_user, num):
    try:
        num = int(num)
    except ValueError:
        return jsonify("Server Error: Invalid num value. Please provide a valid integer num.")

    todo = todoList.query.filter_by(user_ID=current_user.username, num=num).first()
    if todo is None:
        return jsonify("Server Error: TODO not found.")

    db.session.delete(todo)
    db.session.commit()
    return jsonify("Server Success: TODO has been deleted.")

# Mark a TO-DO item as completed
@app.route('/todo/<num>/status', methods=['PUT'])
@token_required
def todo_update_status(current_user, num):
    try:
        num = int(num)
    except ValueError:
        return jsonify("Server Error: Invalid num value. Please provide a valid integer num.")

    todo = todoList.query.filter_by(user_ID=current_user.username, num=num).first()
    if todo is None:
        return jsonify("Server Error: TODO not found.")

    status = request.get_json().get('status')

    todo.status = status
    db.session.commit()
    return jsonify("Server Success: TODO status has been updated.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
