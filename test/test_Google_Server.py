import flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, redirect, url_for, session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from google_auth_oauthlib.flow import Flow
import ssl

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "a_very_long_random_string_of_characters"  # Set a secret key for session management

# Configure the database connection
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///TODO_list.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<User {0}>'.format(self.user_id)

# Configure the Google OAuth flow
CLIENT_SECRETS_FILE = "google_client_secret.json"  # Replace with the path to your client secrets JSON file obtained from the Google Developer Console
SCOPES = ['https://www.googleapis.com/auth/userinfo.email']
FLOW = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri="https://localhost:5000/google_auth_callback"
)

# Define the TO-DO List model
class todoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_ID = db.Column(db.String(100), nullable=False)
    num = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    date_Created = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<todoList {0}>'.format(self.title)

with app.app_context():
    db.create_all()

# Start Up Page
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Backend Software Engine Take Home Test</h1>
                <p>Python, REST API, Flask, SQLAlchemy</p>'''

# Handle the Google authentication callback
@app.route('/google_auth_callback', methods=['GET'])
def google_auth_callback():
    # Retrieve the authorization code from the request
    code = request.args.get('code')

    if code is None:
        # If code is not present, check for authorization_response
        print('gg')
        print(request)
        authorization_response = request.url

        # Fetch the token using authorization_response instead of code
        token = FLOW.fetch_token(authorization_response=authorization_response)
    else:
        # Fetch the token using the code
        print('ggggggggg')
        token = FLOW.fetch_token(code=code)

    id_token_info = id_token.verify_oauth2_token(token['id_token'], google_requests.Request())

    # Retrieve the user ID from the ID token
    user_id = id_token_info['sub']

    # Check if the user exists in the database
    user = User.query.filter_by(user_id=user_id).first()

    if user is None:
        # Create a new user entry in the database
        new_user = User(user_id=user_id)
        db.session.add(new_user)
        db.session.commit()

    # Store the user ID in the session
    session['user_id'] = user_id

    return redirect(url_for('home'))

@app.route('/user/authenticated', methods=['GET'])
def check_authenticated():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({"authenticated": False})
    else:
        return jsonify({"authenticated": True})

# List All TO-DO items
@app.route('/todo/all', methods=['GET'])
def todo_all():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify("Server Error: User not authenticated.")

    todo_list = todoList.query.filter_by(user_ID=user_id).all()
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
def todo_insert():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify("Server Error: User not authenticated.")

    todo_data = request.get_json()
    todo = todoList(user_ID=user_id, **todo_data)
    db.session.add(todo)
    db.session.commit()
    return jsonify("Server Success: TODO has been added.")

# Delete a TO-DO item
@app.route("/todo/<num>", methods=["DELETE"])
def todo_delete(num):
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify("Server Error: User not authenticated.")

    try:
        num = int(num)
    except ValueError:
        return jsonify("Server Error: Invalid num value. Please provide a valid integer num.")

    todo = todoList.query.filter_by(user_ID=user_id, num=num).first()
    if todo is None:
        return jsonify("Server Error: TODO not found.")

    db.session.delete(todo)
    db.session.commit()
    return jsonify("Server Success: TODO has been deleted.")

# Mark a TO-DO item as completed
@app.route('/todo/<num>/status', methods=['PUT'])
def todo_update_status(num):
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify("Server Error: User not authenticated.")

    try:
        num = int(num)
    except ValueError:
        return jsonify("Server Error: Invalid num value. Please provide a valid integer num.")

    todo = todoList.query.filter_by(user_ID=user_id, num=num).first()
    if todo is None:
        return jsonify("Server Error: TODO not found.")

    status = request.get_json().get('status')

    todo.status = status
    db.session.commit()
    return jsonify("Server Success: TODO status has been updated.")

# Enable HTTPS with the generated certificate and private key
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
#context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(r"C:\Users\R O G\PycharmProjects\Test\certificate.crt", r"C:\Users\R O G\PycharmProjects\Test\private_key.key")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, ssl_context=context)
    #app.run(ssl_context=context)
