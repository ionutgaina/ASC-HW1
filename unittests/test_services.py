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
       
    def test_state_mean_1(self):
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
    
    def test_best5_1(self):
        """
        This test checks the best5 function with the input
        'Percent of adults aged 18 years and older who have an overweight classification'.
        """
        result = json.loads(self.task_service.best5(\
            'Percent of adults aged 18 years and older who have an overweight classification'))
        test_file = open('./tests/best5/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_best5_2(self):
        """
        This test checks the best5 function with the input
        'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'.
        """
        result = json.loads(self.task_service\
            .best5('Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'))
        test_file = open('./tests/best5/2.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {}) 
        
    def test_worst5_1(self):
        """
        This test checks the worst5 function with the input
        'Percent of adults aged 18 years and older who have an overweight classification'.
        """
        result = json.loads(self.task_service\
            .worst5('Percent of adults aged 18 years and older who have an overweight classification'))
        test_file = open('./tests/worst5/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_worst5_2(self):
        """
        This test checks the worst5 function with the input
        'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'.
        """
        result = json.loads(self.task_service\
            .worst5('Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'))
        test_file = open('./tests/worst5/2.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_global_mean_1(self):
        """
        This test checks the global_mean function with the input
        'Percent of adults aged 18 years and older who have an overweight classification'.
        """
        result = json.loads(self.task_service\
            .global_mean('Percent of adults aged 18 years and older who have an overweight classification'))
        test_file = open('./tests/global_mean/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_global_mean_2(self):
        """
        This test checks the global_mean function with the input
        'Percent of adults aged 18 years and older who have obesity'.
        """
        result = json.loads(self.task_service\
            .global_mean('Percent of adults aged 18 years and older who have obesity'))
        test_file = open('./tests/global_mean/2.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_diff_from_mean_1(self):
        """
        This test checks the diff_from_mean function with the input
        'Percent of adults aged 18 years and older who have an overweight classification'.
        """
        result = json.loads(self.task_service\
            .diff_from_mean('Percent of adults aged 18 years and older who have an overweight classification'))
        test_file = open('./tests/diff_from_mean/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_diff_from_mean_2(self):
        """
        This test checks the diff_from_mean function with the input
        'Percent of adults aged 18 years and older who have obesity'.
        """
        result = json.loads(self.task_service\
            .diff_from_mean('Percent of adults aged 18 years and older who have obesity'))
        test_file = open('./tests/diff_from_mean/2.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_state_diff_from_mean_1(self):
        """
        This test checks the state_diff_from_mean function with the input
        'Percent of adults who engage in no leisure-time physical activity' and 'Ohio'.
        """
        result = json.loads(self.task_service\
            .state_diff_from_mean('Percent of adults who engage in no leisure-time physical activity', 'Ohio'))
        test_file = open('./tests/state_diff_from_mean/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_state_diff_from_mean_2(self):
        """
        This test checks the state_diff_from_mean function with the input
        'Percent of adults who engage in no leisure-time physical activity' and 'Texas'.
        """
        result = json.loads(self.task_service\
            .state_diff_from_mean('Percent of adults who engage in no leisure-time physical activity', 'Texas'))
        test_file = open('./tests/state_diff_from_mean/2.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_mean_by_category_1(self):
        """
        This test checks the mean_by_category function with the input
        'Percent of adults who engage in no leisure-time physical activity'.
        """
        result = json.loads(self.task_service\
            .mean_by_category('Percent of adults who engage in no leisure-time physical activity'))
        test_file = open('./tests/mean_by_category/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_mean_by_category_2(self):
        """
        This test checks the mean_by_category function with the input
        'Percent of adults aged 18 years and older who have an overweight classification'.
        """
        result = json.loads(self.task_service\
            .mean_by_category('Percent of adults aged 18 years and older who have an overweight classification'))
        test_file = open('./tests/mean_by_category/2.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_state_mean_by_category_1(self):
        """
        This test checks the state_mean_by_category function with the input
        'Percent of adults who engage in no leisure-time physical activity' and 'Ohio'.
        """
        result = json.loads(self.task_service\
            .state_mean_by_category('Percent of adults who engage in no leisure-time physical activity', 'Ohio'))
        test_file = open('./tests/state_mean_by_category/1.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})
        
    def test_state_mean_by_category_2(self):
        """
        This test checks the state_mean_by_category function with the input
        'Percent of adults aged 18 years and older who have obesity' and 'Tennessee'.
        """
        result = json.loads(self.task_service\
            .state_mean_by_category('Percent of adults aged 18 years and older who have obesity', 'Tennessee'))
        test_file = open('./tests/state_mean_by_category/2.json', 'r', encoding="utf-8")
        test_data = json.load(test_file)
        test_file.close()
        self.assertEqual(DeepDiff(result, test_data, math_epsilon=0.01), {})