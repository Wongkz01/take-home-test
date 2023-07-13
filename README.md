# Backend Software Engine Take Home Test
TODO List - Server
1. Sign in using any one of: gmail, facebook or github login.
2. Add a TODO item.
3. Delete a TODO item.
4. List all TODO items.
5. Mark a TODO item as completed.

Please download the ZIP file for this project and run in any IDE that supports python.

Note: The social authentication is not done therefore alternative login method has been implemented which is the "TODO Account" using the JWT Token.

# Instruction For Running The App

1. Run both TODO_Server.py and TODO_Client.py

2. For first time user, please reset the database. Kindly uncomment the "db.dropall()" and run the TODO_Server.py once. After that comment it back to proceed with the application.

```
# Initialise the database
with app.app_context():
    #db.drop_all()
    db.create_all()
```

3. This will be the main menu on the console where user will just enter which option they want. In this case, user will select TODO Account to proceed with login.

```
--------------------------------------------------------------------------------
Backend Software Engine Take Home Test: TODO-List Server
--------------------------------------------------------------------------------
Please login through one of the account:
1. Gmail
2. Facebook
3. Github
4. TODO Account
5. Shutdown
--------------------------------------------------------------------------------
Option: 
```

4. For a new user, select option 2 and press enter to direct the console to the registration page. For existing user, select option 1 and press enter to direct the console to the login page.

```
--------------------------------------------------------------------------------
TODO Account
--------------------------------------------------------------------------------
Please select one of the options:
1. Login
2. Register
3. Back To Main Menu
Option: 
```

5. The registration page will prompt user to enter a username and password for account creation. If the username existed or the user enter nothing, the console will show the warning messaage and deny the user back to the main menu.

```
--------------------------------------------------------------------------------
Register Your TODO Account
--------------------------------------------------------------------------------
Enter a username: hello world
Enter a password: hello123
************************************************************
Server Success: User registered successfully!
************************************************************
```

6. The login page will prompt user to enter their username and password. If the username or password is wrong, the console will show the warning message and deny the user back to the main menu.

```
--------------------------------------------------------------------------------
Login Your TODO Account
--------------------------------------------------------------------------------
Enter your username: hello world
Enter your password: hello123
************************************************************
Login successful!
************************************************************
```

7. Once login successful, the main menu will show up and user will able to select any of the following option that they desired.

```
--------------------------------------------------------------------------------
Please select one of the option below:
1. Add a TODO item
2. Delete a TODO item
3. List all TODO items
4. Mark a TODO as completed
5. Log Out
--------------------------------------------------------------------------------
Option: 
```

8. When selecting option 1 which is "Add a TODO item", the console will prompt user to enter the title that they wanted to save. Once written and enter, the server will return a message indicating the request is a success.

```
Enter the TODO title to be added: test 123
Server Success: TODO has been added.
************************************************************
System Message: Process has ended. Return to main menu.
************************************************************
```

9. When selecting option 2 which is "Delete a TODO item", the console will prompt user to enter the TODO number which they wanted to delete. User can check the TODO number in option 3.

```
Enter the TODO number to be deleted: 1
Server Success: TODO has been deleted.
************************************************************
System Message: Process has ended. Return to main menu.
************************************************************
```

10. When selecting option 3 which is "List all TODO items", the console will show out the list of TODO items that is saved in the database. After done viewing, press ENTER to return to the main menu.

```
************************************************************
Begin of List
************************************************************

----------------------------------
TODO ID: 6
User ID: hello world
Number: 1
Title: test 123
Status: Complete
Date Created: 13/07/2023 17:33:26
----------------------------------

************************************************************
End of List
************************************************************
Press ENTER to return to main menu...
```

11. When selecting option 4 which is "Mark a TODO as completed", the console will prompt user to enter the TODO number which they wanted to update. ONce udpate, user can check back the list in option 3.

```
Enter the TODO number to be mark as completed: 1
Server Success: TODO status has been updated.
************************************************************
System Message: Process has ended. Return to main menu.
************************************************************
```

12. To log out the account, select option 5 in the main menu to log out and back to the front page of the application.

```
************************************************************
System Message: Account Log Out!
************************************************************
```

13. To shut down the system, select option 5 in the main page to shut down the client system.

```
************************************************************
System Message: System Shutdown!
************************************************************
```

14. Remember to stop the server file as well after stopping the client application.

# Instruction For Testing The App



# Instruction For Building The App


# Interface Documentation

