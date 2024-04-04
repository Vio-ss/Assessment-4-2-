import json
from flask import Flask, jsonify, request, render_template, send_file

app = Flask(__name__, template_folder='template')

# Load tasks from JSON file
def load_tasks():
    with open('db.json', 'r') as file:
        return json.load(file)

# Save tasks to JSON file
def save_tasks(tasks):
    with open('db.json', 'w') as file:
        json.dump(tasks, file, indent=4)

# Route to serve index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()['tasks']
    return jsonify({'tasks': tasks})

# POST new task
@app.route('/tasks', methods=['POST'])
def create_task():
    tasks = load_tasks()['tasks']
    data = request.json
    new_task = {
        'id': tasks[-1]['id'] + 1 if tasks else 1,
        'title': data['title'],
        'description': data['description'],
        'done': False
    }
    tasks.append(new_task)
    save_tasks({'tasks': tasks})
    return jsonify(new_task), 201

# PUT update task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = load_tasks()['tasks']
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        data = request.json
        task.update(data)
        save_tasks({'tasks': tasks})
        return jsonify(task), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

# DELETE task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()['tasks']
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        tasks.remove(task)
        save_tasks({'tasks': tasks})
        return jsonify({'message': 'Task deleted successfully'}), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

        
@app.route('/db.json', methods=['GET'])
def get_db():
    return send_file('db.json')

@app.route('/db.json', methods=['POST'])
def add_db():
    tasks = load_tasks()['tasks']
    data = request.json
    new_task = {
        'id': int(tasks[-1]['id']) + 1 if tasks else 1,
        'title': data['title'],
        'description': data['description'],
        'done': False
    }
    tasks.append(new_task)
    save_tasks({'tasks': tasks})
    return jsonify(new_task), 201


@app.route('/db.json/<int:task_id>', methods=['PUT'])
def update_db(task_id):
    tasks = load_tasks()['tasks']
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        data = request.json
        task.update(data)
        save_tasks({'tasks': tasks})
        return jsonify(task), 200
    else:
        return jsonify({'error': 'Task not found'}), 404

@app.route('/db.json', methods=['DELETE'])
def delete_last_task():
    tasks = load_tasks()['tasks']
    if tasks:
        last_task = tasks[-1]
        tasks.remove(last_task)
        save_tasks({'tasks': tasks})
        return jsonify({'message': 'Last task deleted successfully'}), 200
    else:
        return jsonify({'error': 'No tasks found'}), 404

def load_data():
    with open('db.json', 'r') as file:
        return json.load(file)
    
    # Extract task data based on task_id
    task_data = None
    for task in data['tasks']:
        if task['id'] == task_id:
            task_data = task
            break
    
    # If task_data is found, return it as JSON
    if task_data:
        return jsonify(task_data)
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
