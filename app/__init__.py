"""
This is the main file of the application. It initializes the Flask webserver and the services
"""
import logging
import time
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.services import TaskService

webserver = Flask(__name__)

webserver.logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
    datefmt='%d-%m-%Y %H:%M:%S')
formatter.converter = time.gmtime

webserver.logger.addHandler(RotatingFileHandler('webserver.log', maxBytes=10000, backupCount=10)\
    .setFormatter(formatter))
webserver.logger.setLevel(logging.DEBUG)

webserver.shutdown = False

webserver.tasks_runner = ThreadPool(webserver)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.task_service = TaskService(webserver.data_ingestor, webserver.logger,\
    webserver.tasks_runner)

from app import routes
