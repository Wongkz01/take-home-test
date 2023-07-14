import requests

SERVER_URL = 'http://localhost:5000'

# Step 1: Open the authorization URL in a web browser
auth_url = f"{SERVER_URL}/"
print(f"Open the following URL in a web browser: {auth_url}")

# Step 2: Wait for user authorization and retrieve the code from the callback URL
code = input("Enter the code from the callback URL: ")

# Step 3: Exchange the code for an access token
token_url = f"{SERVER_URL}/callback?code={code}"
response = requests.get(token_url)
data = response.json()

# Step 4: Get the username from the server response
username = data.get('username')
print(f"GitHub username: {username}")
