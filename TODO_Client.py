import requests
from datetime import datetime

# http://127.0.0.1:5000
def home_page():
    url = 'http://localhost:5000/'

    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error: {response.status_code} - {response.reason}")

# To display all TO-DO item
def all_todo(token, username):
    url = 'http://localhost:5000/todo/all'
    headers = {'Authorization': token, 'User-ID': username}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        todo_list = response.json()

        for todo in todo_list:
            print(f"TODO ID: {todo['id']}")
            print(f"User ID: {todo['user_ID']}")
            print(f"Number: {todo['num']}")
            print(f"Title: {todo['title']}")
            print(f"Status: {todo['status']}")
            print(f"Date Created: {todo['date_Created']}")
            print("----------------------------------")

    else:
        print("Error:", response.text)

# To add a TO-DO item
def add_todo(title, token, username):
    url = 'http://localhost:5000/todo'
    headers = {'Authorization': token, 'User-ID': username}

    response_all = requests.get(url + '/all', headers=headers)

    if response_all.status_code == 200:
        todo_list = response_all.json()

        max_num = max(int(todo["num"]) for todo in todo_list) if todo_list else 0
        new_num = max_num + 1

        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        new_todo = {
            "user_ID": username,
            "num": new_num,
            "title": title,
            "status": "Pending",
            "date_Created": current_time,
        }

        response_add = requests.post(url, json=new_todo, headers=headers)

        if response_add.status_code == 200:
            print(response_add.json())
        else:
            print(f"Error: {response_add.text}")

    else:
        print(f"Error: {response_all.text}")

# To delete a TO-DO item
def delete_todo(num, token, username):
    if num != "":
        url = f"http://localhost:5000/todo/{num}"
        headers = {'Authorization': token, 'User-ID': username}

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.text}")
    else:
        print("Error: Empty id value. Please provide a valid integer id.")

# To update a TO-DO status
def update_todo(num, token, username):
    if num != "":
        new_status = "Complete"
        url = f"http://localhost:5000/todo/{num}/status"
        headers = {'Authorization': token, 'User-ID': username}

        response = requests.put(url, json={"status": new_status}, headers=headers)

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)
    else:
        print("Error: Empty id value. Please provide a valid integer id.")

# User Home Page
def home(token, username):
    while True:
        print("")
        print("-" * 80)
        print("Please select one of the option below:")
        print("1. Add a TODO item")
        print("2. Delete a TODO item")
        print("3. List all TODO items")
        print("4. Mark a TODO as completed")
        print("5. Log Out")
        print("-" * 80)
        option = input("Option: ")
        print("")

        if option == "1":
            title = input("Enter the TODO title to be added: ")
            add_todo(title, token, username)
            print("*" * 60)
            print("System Message: Process has ended. Return to main menu.")
            print("*" * 60)

        elif option == "2":
            num = input("Enter the TODO number to be deleted: ")
            delete_todo(num, token, username)
            print("*" * 60)
            print("System Message: Process has ended. Return to main menu.")
            print("*" * 60)

        elif option == "3":
            print("*" * 60)
            print("Begin of List")
            print("*" * 60 + "\n")
            print("----------------------------------")
            all_todo(token, username)
            print("\n" + "*" * 60)
            print("End of List")
            print("*" * 60)
            input("Press ENTER to return to main menu...")

        elif option == "4":
            num = input("Enter the TODO number to be mark as completed: ")
            update_todo(num, token, username)
            print("*" * 60)
            print("System Message: Process has ended. Return to main menu.")
            print("*" * 60)

        elif option == "5":
            print("*" * 60)
            print("System Message: Account Log Out!")
            print("*" * 60)
            break
        else:
            print("*" * 60)
            print("Input Error: Please select one of the option above.")
            print("*" * 60)

def gmail_Authentication():
    print("Go gmail")
    input("Press Enter")
    #home()

def facebook_Authentication():
    print("Go facebook")
    input("Press Enter")
    #home()

def github_Authentication():
    print("Go github")
    input("Press Enter")
    #home()

# Local Authentication
def todoAcc_Authentication():
    token = None

    while True:
        print("-" * 80)
        print("TODO Account")
        print("-" * 80)
        print("Please select one of the options:")
        print("1. Login")
        print("2. Register")
        print("3. Back To Main Menu")

        option = input("Option: ")

        if option == "1":
            print("")
            print("-" * 80)
            print("Login Your TODO Account")
            print("-" * 80)
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            response = requests.post('http://localhost:5000/login', auth=(username, password))

            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    print("*" * 60)
                    print("Login successful!")
                    print("*" * 60)
                    break
                else:
                    print("*" * 60)
                    print("Server Error: Token is missing in the response.")
                    print("*" * 60)
                    print("")
            else:
                print("*" * 60)
                print("Login failed. Invalid username or password.")
                print("*" * 60)
                print("")

        elif option == "2":
            print("")
            print("-" * 80)
            print("Register Your TODO Account")
            print("-" * 80)
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            response = requests.post('http://localhost:5000/register', json={'username': username, 'password': password})

            if response.status_code == 201:
                print("*" * 60)
                print(response.json())
                print("*" * 60)
                print("")
                continue
            else:
                print("*" * 60)
                print(response.json())
                print("*" * 60)
                print("")

        elif option == "3":
            print("*" * 60)
            print("System Message: Back To Main Menu")
            print("*" * 60)
            return

        else:
            print("*" * 60)
            print("Input Error: Please select one of the options above.")
            print("*" * 60)
            print("")

    if token:
        home(token, username)

# Main Function
while True:
    print("")
    print("-" * 80)
    print("Backend Software Engine Take Home Test: TODO-List Server")
    print("-" * 80)
    print("Please login through one of the account:")
    print("1. Gmail")
    print("2. Facebook")
    print("3. Github")
    print("4. TODO Account")
    print("5. Shutdown")
    print("-" * 80)
    option = input("Option: ")
    print("")

    if option == "1":
        gmail_Authentication()
    elif option == "2":
        facebook_Authentication()
    elif option == "3":
        github_Authentication()
    elif option == "4":
        todoAcc_Authentication()
    elif option == "5":
        print("*" * 60)
        print("System Message: System Shutdown!")
        print("*" * 60)
        break
    else:
        print("*" * 60)
        print("Input Error: Please select one of the option above.")
        print("*" * 60)
