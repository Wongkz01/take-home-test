import requests
from datetime import datetime
import webbrowser
from flask import session

# https://127.0.0.1:5000
def home_page():
    url = 'https://localhost:5000/'

    response = requests.get(url)
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error: {response.status_code} - {response.reason}")

# To display all TO-DO item
def all_todo():
    response = requests.get('https://localhost:5000/todo/all')

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
def add_todo(title):
    response_all = requests.get('https://localhost:5000/todo/all')

    if response_all.status_code == 200:
        todo_list = response_all.json()

        max_id = max(int(todo["id"]) for todo in todo_list) if todo_list else 0
        new_id = max_id + 1
        max_num = max(int(todo["num"]) for todo in todo_list) if todo_list else 0
        new_num = max_num + 1
        current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Retrieve user ID from session
        user_id = session.get('user_id')

        new_book = {
            "id": new_id,
            "user_ID": user_id,
            "num": new_num,
            "title": title,
            "status": "Pending",
            "date_Created": current_time,
        }

        response_add = requests.post('https://localhost:5000/todo', json=new_book)

        if response_add.status_code == 200:
            print(response_add.json())
        else:
            print(f"Error: {response_add.text}")

    else:
        print(f"Error: {response_all.text}")

# To delete a TO-DO item
def delete_todo(num):
    if num != "":
        url = f"https://localhost:5000/todo/{num}"
        response = requests.delete(url)

        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: {response.text}")
    else:
        print("Error: Empty id value. Please provide a valid integer id.")

# To update a TO-DO status
def update_todo(num):
    if num != "":
        new_status = "Complete"
        url = f"https://localhost:5000/todo/{num}/status"
        response = requests.put(url, json={"status": new_status})

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)
    else:
        print("Error: Empty id value. Please provide a valid integer id.")

# User Home Page
def home():
    # Check if the user is authenticated
    response = requests.get('https://localhost:5000/user/authenticated')
    if response.status_code == 200 and response.json()["authenticated"]:
        # User is authenticated, proceed with home page
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
                add_todo(title)
                print("*" * 60)
                print("System Message: Process has ended. Return to main menu.")
                print("*" * 60)

            elif option == "2":
                num = input("Enter the TODO number to be deleted: ")
                delete_todo(num)
                print("*" * 60)
                print("System Message: Process has ended. Return to main menu.")
                print("*" * 60)

            elif option == "3":
                print("*" * 60)
                print("Begin of List")
                print("*" * 60 + "\n")
                print("----------------------------------")
                all_todo()
                print("\n" + "*" * 60)
                print("End of List")
                print("*" * 60)
                input("Press ENTER to return to main menu...")

            elif option == "4":
                num = input("Enter the TODO number to be mark as completed: ")
                update_todo(num)
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
    else:
        print("User not authenticated. Returning to main menu.")

def gmail_Authentication():
    # Redirect the user to the Google authentication URL
    auth_url = 'https://localhost:5000/google_auth_callback'
    webbrowser.open(auth_url)

    # Check if the user is authenticated
    response = requests.get('https://localhost:5000/user/authenticated', verify=False)
    if response.status_code == 200 and response.json()["authenticated"]:
        input("Your authentication is valid. Press ENTER to proceed... ")
        home()
    else:
        print("Authentication failed. Returning to main menu.")

def facebook_Authentication():
    print("Go facebook")
    input("Press Enter")
    home()

def github_Authentication():
    print("Go github")
    input("Press Enter")
    home()

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
    print("4. Shutdown")
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
        print("*" * 60)
        print("System Message: System Shutdown!")
        print("*" * 60)
        break
    else:
        print("*" * 60)
        print("Input Error: Please select one of the option above.")
        print("*" * 60)
