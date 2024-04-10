"""
This file contains the unit tests for the services.py file.
"""
import unittest
import logging
import json
import os
import sys

from deepdiff import DeepDiff

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, '..', 'app'))

from data_ingestor import DataIngestor
from services import TaskService

class TestServices(unittest.TestCase):
    """
    This class contains the unit tests for the services.py file.
    """
    def setUp(self):
        self.data_ingestor = DataIngestor("./data.csv")
        logger = logging.getLogger(__name__)
        self.task_service = TaskService(self.data_ingestor, logger)
    
    def test_states_mean_1(self):
        """
        This test checks the states_mean function with the input 
        'Percent of adults aged 18 years and older who have an overweight classification'.
        """
        result = json.loads(self.task_service\
            .states_mean(\
                'Percent of adults aged 18 years and older who have an overweight classification'))
        test_file = open('./tests/states_mean/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_states_mean_2(self):
        """
        This test checks the states_mean function with the input
        'Percent of adults aged 18 years and older who have obesity'.
        """
        result = json.loads(self.task_service\
            .states_mean('Percent of adults aged 18 years and older who have obesity'))
        test_file = open('./tests/states_mean/2.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
       
    def test_state_mean(self):
        """
        This test checks the state_mean function with the input 'Ohio'
        and 'Percent of adults who engage in no leisure-time physical activity'.
        """
        result = json.loads(self.task_service.state_mean(\
            'Percent of adults who engage in no leisure-time physical activity', 'Ohio'))
        test_file = open('./tests/state_mean/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        