"""
This file is the entry point of the application. It initializes the Flask 
web server and imports the routes module.
"""
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.services import TaskService

webserver = Flask(__name__)
webserver.shutdown = False
webserver.tasks_runner = ThreadPool(webserver)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.task_service = TaskService(webserver.data_ingestor, webserver)

from app import routes
