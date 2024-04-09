"""
Module docstring: This module defines routes for the webserver.
"""

from flask import request, jsonify, json
from app import webserver


@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """
    A POST endpoint that receives data and returns it back as a response.
    """
    if request.method == 'POST':
        data = request.json
        print(f"got data in post {data}")

        response = {"message": "Received data successfully", "data": data}

        return jsonify(response), 200
    return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    A GET endpoint that returns the results of a task given a job_id.
    """
    print(f"JobID is {job_id}")

    job_id = int(job_id)

    if job_id < 1 or job_id > len(webserver.tasks_runner.tasks):
        return jsonify({
            'status': 'error',
            'reason': 'Invalid job_id'
        })

    task = webserver.tasks_runner.tasks[job_id - 1]

    if task.status == "running":
        return jsonify({'status': 'running'})

    with open(f"results/job_{job_id}.json", "r", encoding="utf-8") as f:
        result = json.load(f)

    return jsonify({'status': 'done', 'data': result})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    A POST endpoint that receives a question and returns the mean of the data values for each state.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner.add_task(webserver.task_service.states_mean, data['question'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    A POST endpoint that receives a question and a state and 
    returns the mean of the data values for that state.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.state_mean, data['question'], data['state'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503

    return jsonify({"job_id": job_id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    A POST endpoint that receives a question and returns the 5 states with the best data values.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner.add_task(webserver.task_service.best5, data['question'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503
    return jsonify({"job_id": job_id})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    A POST endpoint that receives a question and returns the 5 states with the worst data values.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner.add_task(webserver.task_service.worst5, data['question'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503

    return jsonify({"job_id": job_id})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    A POST endpoint that receives a question and returns the global mean of the data values.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner.add_task(webserver.task_service.global_mean, data['question'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503

    return jsonify({"job_id": job_id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    A POST endpoint that receives a question and
    returns the difference of the data values from the mean.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.diff_from_mean, data['question'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    A POST endpoint that receives a question and a state and 
    returns the difference of the data values from the mean for that state.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.state_diff_from_mean, data['question'], data['state'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503

    return jsonify({"job_id": job_id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    A POST endpoint that receives a question and 
    returns the mean of the data values for each category.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.mean_by_category, data['question'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503

    return jsonify({"job_id": job_id})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    A POST endpoint that receives a question and a state and 
    returns the mean of the data values for each category for that state.
    """
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.state_mean_by_category, data['question'], data['state'])

    if job_id is None:
        return jsonify({"error": "Server is shutting down"}), 503

    return jsonify({"job_id": job_id})


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def shutdown_gracefully():
    """
    A GET endpoint that shuts down the server gracefully.
    """
    print("Shutting down gracefully")

    webserver.shutdown = True

    return jsonify({"message": "OK"}), 200


@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    """
    A GET endpoint that returns all the jobs in the thread pool.
    """
    return jsonify({'status': 'done', 'data': webserver.task_service.jobs()})


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """
    A GET endpoint that returns the number of jobs in the thread pool.
    """
    return jsonify({'data': webserver.task_service.num_jobs()})


@webserver.route('/')
@webserver.route('/index')
def index():
    """
    A GET endpoint that returns the defined routes.
    """
    routes = get_defined_routes()

    paragraphs = []
    for route in routes:
        paragraphs.append(f"<p>{route}</p>")

    return "".join(paragraphs)


def get_defined_routes():
    """
    Get all the defined routes in the webserver.
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
