from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from app.services import TaskService

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.task_service = TaskService(webserver.data_ingestor, webserver)

from app import routes