from flask import Flask, redirect, request, jsonify
import requests

app = Flask(__name__)
CLIENT_ID = '86ac12c569295ae2d1bf'
CLIENT_SECRET = 'ef04cb9927eab6d58bd35ea166cb1c393597f21c'


@app.route('/')
def home():
    return redirect(f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}")


@app.route('/callback')
def callback():
    code = request.args.get('code')
    token = get_access_token(code)
    username = get_username(token)
    return jsonify({'username': username})


def get_access_token(code):
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code
    }
    headers = {
        'Accept': 'application/json'
    }
    response = requests.post('https://github.com/login/oauth/access_token', json=payload, headers=headers)
    return response.json().get('access_token')


def get_username(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.github.com/user', headers=headers)
    return response.json().get('login')


if __name__ == '__main__':
    app.run(debug=True)
