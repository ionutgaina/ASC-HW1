import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.services import TaskService

webserver = Flask(__name__)

webserver.logger.addHandler(RotatingFileHandler('webserver.log', maxBytes=10000, backupCount=10))
webserver.logger.setLevel(logging.DEBUG)

webserver.shutdown = False

webserver.tasks_runner = ThreadPool(webserver)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.task_service = TaskService(webserver.data_ingestor, webserver.logger, webserver.tasks_runner)

from app import routes