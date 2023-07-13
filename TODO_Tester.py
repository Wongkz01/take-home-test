import pytest
import subprocess
import time

# # Start the server in a separate process
# def start_server():
#     subprocess.Popen(["python", "TODO_Server.py"])
#
# # Stop the server process
# def stop_server():
#     subprocess.Popen(["pkill", "-f", "TODO_Server.py"])
#
# @pytest.fixture(scope='session', autouse=True)
# def setup_server():
#     start_server()
#     # Wait for the server to start
#     time.sleep(1)
#
#     yield
#
#     stop_server()

import requests
from datetime import datetime

# Note:
# Start up the TODO_Server manually
# The database should be empty as the test code are used to test for a new user, not existing user
# To run the tester, kindly drop the database and create it again on the server side

def test_home_page():
    url = 'http://localhost:5000/'
    response = requests.get(url)
    assert response.status_code == 200
    assert "Backend Software Engine Take Home Test" in response.text

# Note: The test_register will fail if the account existed where it will return status code 400
def test_register():
    url = 'http://localhost:5000/register'
    data = {'username': 'testuser', 'password': 'testpass'}
    response = requests.post(url, json=data)
    assert response.status_code == 201
    assert response.json() == "Server Success: User registered successfully!"

    # Test duplicate registration
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert response.json() == "Server Error: Username already exist!"

def test_login():
    url = 'http://localhost:5000/login'
    data = {'username': 'testuser', 'password': 'testpass'}
    response = requests.post(url, auth=('testuser', 'testpass'))
    assert response.status_code == 200
    assert 'token' in response.json()

    # Test invalid login
    response = requests.post(url, auth=('testuser', 'wrongpass'))
    assert response.status_code == 401
    assert response.json() == "Server Error: Invalid username and password!"

# Note: The test_todo_all will fail if the TO-DO item is already added once for this user
# Because the "num" has been hard coded as "1" for the first TO-DO item
def test_todo_all():
    # Register a test user
    register_url = 'http://localhost:5000/register'
    register_data = {'username': 'testuser', 'password': 'testpass'}
    requests.post(register_url, json=register_data)

    # Login to get the token
    login_url = 'http://localhost:5000/login'
    login_response = requests.post(login_url, auth=('testuser', 'testpass'))
    token = login_response.json().get('token')

    # Add a TO-DO item
    todo_url = 'http://localhost:5000/todo'
    todo_data = {
        "user_ID": "testuser",
        "num": 1,
        "title": "Test Todo",
        "status": "Pending",
        "date_Created": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    headers = {'Authorization': token}
    requests.post(todo_url, json=todo_data, headers=headers)

    # Get all TO-DO items
    all_url = 'http://localhost:5000/todo/all'
    headers = {'Authorization': token}
    response = requests.get(all_url, headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_todo_insert():
    # Register a test user
    register_url = 'http://localhost:5000/register'
    register_data = {'username': 'testuser', 'password': 'testpass'}
    requests.post(register_url, json=register_data)

    # Login to get the token
    login_url = 'http://localhost:5000/login'
    login_response = requests.post(login_url, auth=('testuser', 'testpass'))
    token = login_response.json().get('token')

    # Add a TO-DO item
    todo_url = 'http://localhost:5000/todo'
    todo_data = {
        "user_ID": "testuser",
        "num": 2,
        "title": "Test Todo",
        "status": "Pending",
        "date_Created": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    headers = {'Authorization': token}
    response = requests.post(todo_url, json=todo_data, headers=headers)
    assert response.status_code == 200
    assert response.json() == "Server Success: TODO has been added."

def test_todo_delete():
    # Register a test user
    register_url = 'http://localhost:5000/register'
    register_data = {'username': 'testuser', 'password': 'testpass'}
    requests.post(register_url, json=register_data)

    # Login to get the token
    login_url = 'http://localhost:5000/login'
    login_response = requests.post(login_url, auth=('testuser', 'testpass'))
    token = login_response.json().get('token')

    # Add a TO-DO item
    todo_url = 'http://localhost:5000/todo'
    todo_data = {
        "user_ID": "testuser",
        "num": 3,
        "title": "Test Todo 3",
        "status": "Pending",
        "date_Created": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    headers = {'Authorization': token}
    requests.post(todo_url, json=todo_data, headers=headers)

    # Delete the TO-DO item
    delete_url = 'http://localhost:5000/todo/3'
    response = requests.delete(delete_url, headers=headers)
    assert response.status_code == 200
    assert response.json() == "Server Success: TODO has been deleted."

def test_todo_update_status():
    # Register a test user
    register_url = 'http://localhost:5000/register'
    register_data = {'username': 'testuser', 'password': 'testpass'}
    requests.post(register_url, json=register_data)

    # Login to get the token
    login_url = 'http://localhost:5000/login'
    login_response = requests.post(login_url, auth=('testuser', 'testpass'))
    token = login_response.json().get('token')

    # Add a TO-DO item
    todo_url = 'http://localhost:5000/todo'
    todo_data = {
        "user_ID": "testuser",
        "num": 4,
        "title": "Test Todo 4",
        "status": "Pending",
        "date_Created": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }
    headers = {'Authorization': token}
    requests.post(todo_url, json=todo_data, headers=headers)

    # Update the status of the TO-DO item
    update_url = 'http://localhost:5000/todo/4/status'
    new_status = "Complete"
    response = requests.put(update_url, json={"status": new_status}, headers=headers)
    assert response.status_code == 200
    assert response.json() == "Server Success: TODO status has been updated."
