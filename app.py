from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = {}
task_id_counter = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    if not request.json or 'name' not in request.json:
        return jsonify({'error': 'Bad Request', 'message': 'Task name is required'}), 400
    task_data = {
        'id': task_id_counter,
        'name': request.json['name'],
        'description': request.json.get('description', "")
    }
    tasks[task_id_counter] = task_data
    task_id_counter += 1
    return jsonify(task_data), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Not Found', 'message': 'Task not found'}), 404
    if not request.json:
        return jsonify({'error': 'Bad Request', 'message': 'Request body must be JSON'}), 400
    task_data = tasks[task_id]
    task_data['name'] = request.json.get('name', task_data['name'])
    task_data['description'] = request.json.get('description', task_data['description'])
    tasks[task_id] = task_data
    return jsonify(task_data), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Not Found', 'message': 'Task not found'}), 404
    del tasks[task_id]
    return '', 204

@app.route('/tasks', methods=['GET'])
def view_tasks():
    return jsonify(list(tasks.values())), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

