import requests
import json
import unittest
import logging

import os

import sys
try:
    from io import StringIO
except:
    from StringIO import StringIO

from deepdiff import DeepDiff

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, '..', 'app'))
from data_ingestor import DataIngestor
from services import TaskService

class TestServices(unittest.TestCase):
    def setUp(self):
        self.data_ingestor = DataIngestor("./data.csv")
        logger = logging.getLogger(__name__)
        self.task_service = TaskService(self.data_ingestor, logger)
    
    def test_states_mean(self):
        result = json.loads(self.task_service.states_mean('Percent of adults aged 18 years and older who have an overweight classification'))
        
        test_file = open('./tests/states_mean/1.json', 'r')
        test_data = json.load(test_file)
        test_file.close()
        
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
        
        
        