from app import webserver
from flask import request, jsonify

import os
import json

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    
    job_id = int(job_id)
    
    if job_id < 1 or job_id > len(webserver.tasks_runner.tasks):
        return jsonify({
            'status': 'error',
            'reason': 'Invalid job_id'
        })
        
    task = webserver.tasks_runner.tasks[job_id - 1]
        
    if task.status == "running":
        return jsonify({
            'status': 'running'
        })
            
    with open(f"results/job_{job_id}.json", "r") as f:
        result = json.load(f)
        
    return jsonify({
        'status': 'done',
        'data': result
    })


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    data = request.json
    print(f"Got request {data}")
    
    job_id = webserver.tasks_runner.add_task(webserver.task_service.states_mean, data['question'])
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    data = request.json
    print(f"Got request {data}")
    
    job_id = webserver.tasks_runner.add_task(webserver.task_service.state_mean, data['question'], data['state'])
    return jsonify({"job_id": job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    data = request.json
    print(f"Got request {data}")
    
    job_id = webserver.tasks_runner.add_task(webserver.task_service.best5, data['question'])
    return jsonify({"job_id": job_id})

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    data = request.json
    print(f"Got request {data}")
    
    job_id = webserver.tasks_runner.add_task(webserver.task_service.worst5, data['question'])
    return jsonify({"job_id": job_id})

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    data = request.json
    print(f"Got request {data}")
    
    job_id = webserver.tasks_runner.add_task(webserver.task_service.global_mean, data['question'])
    return jsonify({"job_id": job_id})

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request(): 
    data = request.json
    print(f"Got request {data}")
    
    job_id = webserver.tasks_runner.add_task(webserver.task_service.diff_from_mean, data['question'])
    return jsonify({"job_id": job_id})

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    data = request.json
    print(f"Got request {data}")
    
    job_id = webserver.tasks_runner.add_task(webserver.task_service.state_diff_from_mean, data['question'], data['state'])
    return jsonify({"job_id": job_id})

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    # TODO
    # Get request data
    # Register job. Don't wait for task to finish
    # Increment job_id counter
    # Return associated job_id

    return jsonify({"status": "NotImplemented"})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
