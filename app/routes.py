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
    webserver.logger.info("Received a POST request to /api/post_endpoint")
    if request.method == 'POST':
        data = request.json
        webserver.logger.info("Received data for POST request to /api/post_endpoint: %s", data)

        response = {"message": "Received data successfully", "data": data}

        webserver.logger.info("Sending response for POST request to /api/post_endpoint: %s", \
            response)
        return jsonify(response), 200
    response = {"error": "Method not allowed"}
    webserver.logger.info("Sending response for POST request to /api/post_endpoint: %s", response)
    return jsonify(response), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """
    A GET endpoint that returns the results of a task given a job_id.
    """
    webserver.logger.info("Received a GET request to /api/get_results/%s", job_id)
    job_id = int(job_id)

    if job_id < 1 or job_id > len(webserver.tasks_runner.tasks):
        response = {"status": "error", "reason": "Invalid job_id"}
        webserver.logger.info("Sending response for GET request to /api/get_results/%s: %s", \
            job_id, response)
        return jsonify(response)

    task = webserver.tasks_runner.tasks[job_id - 1]

    if task.status == "running":
        response = {"status": "running"}
        webserver.logger.info("Sending response for GET request to /api/get_results/%s: %s", \
            job_id, response)
        return jsonify(response)

    with open(f"results/job_{job_id}.json", "r", encoding="utf-8") as f:
        result = json.load(f)

    response = {"status": "done", "data": result}
    webserver.logger.info("Sending response for GET request to /api/get_results/%s: %s", \
        job_id, response)
    return jsonify(response)


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """
    A POST endpoint that receives a question and returns the mean of the data values for each state.
    """
    webserver.logger.info("Received a POST request to /api/states_mean")
    webserver.logger.info("Received data for POST request to /api/states_mean: %s", request.json)
    data = request.json

    job_id = webserver.tasks_runner.add_task(webserver.task_service.states_mean, data['question'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger.info("Sending response for POST request to /api/states_mean: %s", response)
        return jsonify({"error": "Server is shutting down"}), 503

    response = {"job_id": job_id}
    webserver.logger.info("Sending response for POST request to /api/states_mean: %s", response)
    return jsonify(response)


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """
    A POST endpoint that receives a question and a state and 
    returns the mean of the data values for that state.
    """
    webserver.logger.info("Received a POST request to /api/state_mean")
    webserver.logger.info("Received data for POST request to /api/state_mean: %s", request.json)
    data = request.json

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.state_mean, data['question'], data['state'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger.info("Sending response for POST request to /api/state_mean: %s", response)
        return jsonify({"error": "Server is shutting down"}), 503

    response = {"job_id": job_id}
    webserver.logger.info("Sending response for POST request to /api/state_mean: %s", response)
    return jsonify(response)


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """
    A POST endpoint that receives a question and returns the 5 states with the best data values.
    """
    webserver.logger.info("Received a POST request to /api/best5")
    webserver.logger.info("Received data for POST request to /api/best5: %s", request.json)
    data = request.json

    job_id = webserver.tasks_runner.add_task(webserver.task_service.best5, data['question'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger.info("Sending response for POST request to /api/best5: %s", response)
        return jsonify(response), 503
    response = {"job_id": job_id}
    webserver.logger.info("Sending response for POST request to /api/best5: %s", response)
    return jsonify(response)


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """
    A POST endpoint that receives a question and returns the 5 states with the worst data values.
    """
    webserver.logger.info("Received a POST request to /api/worst5")
    webserver.logger.info("Received data for POST request to /api/worst5: %s", request.json)
    data = request.json

    job_id = webserver.tasks_runner.add_task(webserver.task_service.worst5, data['question'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger.info("Sending response for POST request to /api/worst5: %s", response)
        return jsonify(response), 503

    response = {"job_id": job_id}
    webserver.logger.info("Sending response for POST request to /api/worst5: %s", response)
    return jsonify(response)


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """
    A POST endpoint that receives a question and returns the global mean of the data values.
    """
    webserver.logger.info("Received a POST request to /api/global_mean")
    webserver.logger.info("Received data for POST request to /api/global_mean: %s", request.json)
    data = request.json

    job_id = webserver.tasks_runner.add_task(webserver.task_service.global_mean, data['question'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger.info("Sending response for POST request to /api/global_mean: %s", response)
        return jsonify(response), 503

    response = {"job_id": job_id}
    webserver.logger.info("Sending response for POST request to /api/global_mean: %s", response)
    return jsonify(response)


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """
    A POST endpoint that receives a question and
    returns the difference of the data values from the mean.
    """
    webserver.logger.info("Received a POST request to /api/diff_from_mean")
    webserver.logger.info("Received data for POST request to /api/diff_from_mean: %s", request.json)
    data = request.json

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.diff_from_mean, data['question'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger.info("Sending response for POST request to /api/diff_from_mean: %s", \
            response)
        return jsonify(response), 503

    response = {"job_id": job_id}
    webserver.logger.info("Sending response for POST request to /api/diff_from_mean: %s", response)
    return jsonify(response)

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """
    A POST endpoint that receives a question and a state and 
    returns the difference of the data values from the mean for that state.
    """
    webserver.logger.info("Received a POST request to /api/state_diff_from_mean")
    webserver.logger.info("Received data for POST request to /api/state_diff_from_mean: %s", \
        request.json)
    data = request.json

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.state_diff_from_mean, data['question'], data['state'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger.info("Sending response for POST request to /api/state_diff_from_mean: %s",\
            response)
        return jsonify(response), 503

    response = {"job_id": job_id}
    webserver.logger.info("Sending response for POST request to /api/state_diff_from_mean: %s", \
        response)
    return jsonify(response)


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """
    A POST endpoint that receives a question and 
    returns the mean of the data values for each category.
    """
    webserver.logger.info("Received a POST request to /api/mean_by_category")
    webserver.logger.info("Received data for POST request to /api/mean_by_category: %s", \
        request.json)
    data = request.json

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.mean_by_category, data['question'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger.info("Sending response for POST request to /api/mean_by_category: %s",\
            response)
        return jsonify(response), 503

    response = {"job_id": job_id}
    webserver.logger.info("Sending response for POST request to /api/mean_by_category: %s", \
        response)
    return jsonify(response)


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """
    A POST endpoint that receives a question and a state and 
    returns the mean of the data values for each category for that state.
    """
    webserver.logger.info("Received a POST request to /api/state_mean_by_category")
    webserver.logger.info("Received data for POST request to /api/state_mean_by_category: %s",\
        request.json)
    data = request.json

    job_id = webserver.tasks_runner\
        .add_task(webserver.task_service.state_mean_by_category, data['question'], data['state'])

    if job_id is None:
        response = {"error": "Server is shutting down"}
        webserver.logger\
            .info("Sending response for POST request to /api/state_mean_by_category: %s",response)
        return jsonify(response), 503

    response = {"job_id": job_id}
    webserver.logger\
        .info("Sending response for POST request to /api/state_mean_by_category: %s", response)
    return jsonify(response )


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def shutdown_gracefully():
    """
    A GET endpoint that shuts down the server gracefully.
    """
    webserver.logger.info("Received a GET request to /api/graceful_shutdown")
    webserver.tasks_runner.shutdown()
    response = {"message": "OK"}
    webserver.logger.info("Sending response for GET request to /api/graceful_shutdown: %s",\
        response)
    return jsonify(response), 200


@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    """
    A GET endpoint that returns all the jobs in the thread pool.
    """
    webserver.logger.info("Received a GET request to /api/jobs")
    response = {"status": "done", "data": webserver.task_service.jobs()}
    webserver.logger.info("Sending response for GET request to /api/jobs: %s", response)
    return jsonify(response)


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """
    A GET endpoint that returns the number of jobs in the thread pool.
    """
    webserver.logger.info("Received a GET request to /api/num_jobs")
    response = {'data': webserver.task_service.num_jobs()}
    webserver.logger.info("Sending response for GET request to /api/num_jobs: %s", response)
    return jsonify(response)


@webserver.route('/')
@webserver.route('/index')
def index():
    """
    A GET endpoint that returns the defined routes.
    """
    webserver.logger.info("Received a GET request to /index")
    routes = get_defined_routes()

    paragraphs = []
    for route in routes:
        paragraphs.append(f"<p>{route}</p>")

    response = "".join(paragraphs)
    webserver.logger.info("Sending response for GET request to /index: %s", response)
    return response


def get_defined_routes():
    """
    Get all the defined routes in the webserver.
    """
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
