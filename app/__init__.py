"""
This is the main file of the application. It initializes the Flask webserver and the services
"""
import logging
import logging.handlers
import time
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.services import TaskService

webserver = Flask(__name__)

webserver.logger = logging.getLogger(__name__)
webserver.logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler('webserver.log', maxBytes=10000, backupCount=10)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
    datefmt='%d-%m-%Y %H:%M:%S')
formatter.converter = time.gmtime

handler.setFormatter(formatter)

webserver.logger.addHandler(handler)


webserver.logger.info("Server started")

webserver.shutdown = False

webserver.tasks_runner = ThreadPool(webserver)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.task_service = TaskService(webserver.data_ingestor, webserver.logger,\
    webserver.tasks_runner)

from app import routes
