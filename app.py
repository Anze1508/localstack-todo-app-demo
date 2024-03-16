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
