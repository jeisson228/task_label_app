# task_label_app

So, cursor app helped a lot to ths construction of this app, i have the bases for django and other python frameworks but i also embrace the help of IA to the fast and high quality of app building.

to run this app: put a terminal into the folder where this README.md is,
Run o activate the venv
    .\venv\Scripts\Activate.ps1
next run to run the app
    py manage.py runserver

        {Watching for file changes with StatReloader
        Performing system checks...

        System check identified no issues (0 silenced).
        May 01, 2025 - 10:50:00
        Django version 5.2, using settings 'tasks.settings'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CTRL-BREAK.}

test the opened app opening in a web explorer
    http://127.0.0.1:8000/api/test
        {{
            "message":  "You are connected to the server"
        }}

Now as the app is open, from an server comunication app send the next requests:
All endpoints are POST http method, excluding the task delete and label delete endpoints
This will be urls ""
This will be headers []
This will be bodies ~~
This will be responses ++

Test to create an user:
    "http://localhost:8000/api/auth/register/"
    [Accept: */*
    User-Agent: Thunder Client (https://www.thunderclient.com) #or any, i find vscode-thunderclient less cluttered
    Content-Type: application/json]
    ~{
        "username": "Aldi",
        "password": "pass_123456",
        "email": "Aldi@aakcience.com"
    }~
    =>
    +{
    "token": "998c7d60ee5460cef195d506f0ee61955ce46cd9", #Save this token for the next requests
    "user_id": 3,
    "username": "Aldi"
    }+

Test to create a label:
    "http://localhost:8000/api/labels/create/"
    [Accept: */*
    User-Agent: Thunder Client (https://www.thunderclient.com)
    Authorization: Token 998c7d60ee5460cef195d506f0ee61955ce46cd9
    Content-Type: application/json]
    ~{
        "name": "Aldi_label"
    }~
    =>
    +{
    "id": 3,
    "name": "Aldi_label"
    }+

Test to create a Task
    "http://localhost:8000/api/tasks/create/"
    [Accept: */*
    User-Agent: Thunder Client (https://www.thunderclient.com)
    Authorization: Token 998c7d60ee5460cef195d506f0ee61955ce46cd9
    Content-Type: application/json]
    ~{
    "title": "Aldi_task1",
    "description": "This is a test task",
    "completed": true,
    "labels": [2]
    }~
    =>
    +{
    "id": 6,
    "title": "Aldi_task1",
    "description": "This is a test task",
    "completed": true,
    "labels": [2]
    }+

Test to update a Task:
    You can use the same create task endpoint; i designed this un purpose because it will get a "INSERT ... ON DUPLICATE KEY UPDATE"
    kind of endpoint, it will be easier for a frontend to manage tasks this way
    It works by searching the same task title to the same owner, change the json requested and check how it updates the task internally
    the task can have no labels, but the other attributes are needed


Test to delete a Task:
    "http://localhost:8000/api/tasks/delete/" this is a DELETE http method
    [Accept: */*
    User-Agent: Thunder Client (https://www.thunderclient.com)
    Authorization: Token 998c7d60ee5460cef195d506f0ee61955ce46cd9
    Content-Type: application/json]
    ~{
    "title": "Aldi_task1"
    }~
    =>
    +{
    "message": "Task \"Aldi_task1\" deleted successfully"
    }+

Test to delete a Task:
    "http://localhost:8000/api/labels/delete/" this is a DELETE http method
    [Accept: */*
    User-Agent: Thunder Client (https://www.thunderclient.com)
    Authorization: Token 998c7d60ee5460cef195d506f0ee61955ce46cd9
    Content-Type: application/json]
    ~{
    "name": "Aldi_label"
    }~
    =>
    +{
    "message": "Label \"Aldi_label\" deleted successfully"
    }+

The app has an Login endpoint in case you want to get the token again
    "http://localhost:8000/api/auth/login/"
    [Accept: */*
    User-Agent: Thunder Client (https://www.thunderclient.com)]
    ~{
        "username": "Aldi",
        "password": "pass_123456"
    }~
    =>
    +{
    "token": "998c7d60ee5460cef195d506f0ee61955ce46cd9",
    "user_id": 3,
    "username": "Aldi"
    }+