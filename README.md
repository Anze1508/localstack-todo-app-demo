# Creating a basic ToDO List Application

This application will allow users to create, list and delete tasks. 

## Prerequisites

- LocalStack installed and running.
- AWS CLI installed and configured to use LocalStack.
- Python and pip installed.
- Basic familiarity with terminal or command prompt.

## Step 1: Setup LocalStack and create a DynamoDB Table

1. Start LocalStack.
2. Create a DynamoDB table named "Tasks" with a primary key "taskId":

```
awslocal dynamodb create-table \
    --table-name Tasks \
    --attribute-definitions AttributeName=taskId,AttributeType=S \
    --key-schema AttributeName=taskId,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

```

## Step 2: Develop API Server

1. Install Flask:

```
pip install Flask boto3
```

2. Create app.py: In Visual Studio Code, create a file named app.py. This file will contain your Flask application.

3. Write Your Flask Application: Copy the following basic Flask application into app.py. This code provides endpoints to create, list, and delete tasks in the DynamoDB table.

```
from flask import Flask, request, jsonify
import boto3
import uuid

app = Flask(__name__)

# Initialize a DynamoDB client
dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:4566")

@app.route('/tasks', methods=['GET'])
def list_tasks():
    response = dynamodb.scan(TableName='Tasks')
    tasks = [{'taskId': item['taskId']['S'], 'description': item['description']['S']} for item in response['Items']]
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    task_id = str(uuid.uuid4())
    description = request.json.get('description', '')
    dynamodb.put_item(TableName='Tasks', Item={'taskId': {'S': task_id}, 'description': {'S': description}})
    return jsonify({'taskId': task_id, 'description': description})

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    dynamodb.delete_item(TableName='Tasks', Key={'taskId': {'S': task_id}})
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)

```

## Step 3: Run your API Server

Run your Flask application:
```
FLASK_APP=app.py flask run
```

## Step 4: Testing the application

1. List all tasks
```
curl http://localhost:5000/tasks
```

2. Create a new task

Replace "Your task description here" with the description of the task you want to add.

```
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d '{"description": "Your task description here"}'
```

3. Delete a task
Replace <task_id> with the ID of the task you want to delete. You can get the task ID from the list tasks command.
```
curl -X DELETE http://localhost:5000/tasks/<task_id>
```

# More information about the project

## What is Flask?

_Flask is a lightweight WSGI (Web Server Gateway Interface) web application framework in Python. It's designed to make getting started quick and easy, with the ability to scale up to complex applications. In your project, Flask is used to create a simple web server that can handle HTTP requests. You've defined routes (URL paths) that the server listens to, and when a request is made to one of these routes, Flask executes a function (known as a view function) that processes the request and returns a response. This response can be a simple message, data in JSON format, or an HTML page, depending on what the function is programmed to return._

## How does Flask work with LocalStack?

_LocalStack provides a local simulation of AWS cloud services, such as DynamoDB. When you're developing applications that use AWS services, you would normally need to interact with the actual AWS cloud, which could incur costs and require internet access. LocalStack, however, simulates these services on your local machine, allowing you to develop and test your applications without connecting to AWS directly._

## In this project, the Flask application interacts with DynamoDB not in the AWS cloud, but with the LocalStack simulation of DynamoDB. This setup is beneficial for several reasons:

1. Cost: You can develop and test applications using AWS services without incurring any costs.
2. Development Speed: You can quickly test changes locally without deploying them to AWS.
3. Offline Development: You can work without an internet connection, as the services are simulated locally.

## Integration explained

The Flask app integrates with LocalStack (simulating DynamoDB) in the following way:
- The Flask app uses the boto3 library (AWS's SDK for Python) to interact with AWS services. Normally, boto3 would connect to the actual AWS services over the internet.
- By specifying endpoint_url="http://localhost:4566" in the boto3 client setup, you're directing boto3 to communicate with LocalStack's simulation of DynamoDB running on your local machine instead of the real AWS DynamoDB service. LocalStack listens on port 4566 for requests to AWS services it simulates.
- When your Flask app needs to create, list, or delete tasks, it makes requests to LocalStack's DynamoDB service. LocalStack processes these requests as if they were made to the real DynamoDB, but everything occurs locally on your machine.
