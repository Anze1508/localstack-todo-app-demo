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
    --key-schema AttributeName=taskId,KeyType=HASH \
    --attribute-definitions AttributeName=taskId,AttributeType=S \
    --billing-mode PAY_PER_REQUEST \
    --region ap-south-1
```

## Step 2: Develop API Server

1. Install Flask:

```
pip install Flask boto3
```




