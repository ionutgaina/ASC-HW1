"""
Module docstring: This module defines services for the webserver.
"""
from flask import json

class TaskService:
    """
    Service class responsible for handling tasks related to data analysis.
    """

    def __init__(self, data_ingestor, app=None):
        """
        Initializes TaskService with a data_ingestor instance and an optional Flask app instance.
        """
        self.data_ingestor = data_ingestor
        self.app = app

    def question_data(self, question):
        """
        Retrieves data for a specific question from the data_ingestor.
        """
        self.app.logger.info('Entered method question_data with parameter: %s', question)
        data = self.data_ingestor.get_data()
        data = data[data['Question'] == question]
        self.app.logger.info('Method question_data returned: %s', question)
        return data

    def is_best(self, question):
        """
        Checks if the given question is best when the value is maximum.
        """
        self.app.logger.info('Entered method is_best with parameter %s', question)
        if self.data_ingestor.get_questions_best_is_min().count(question):
            self.app.logger.info('Method is_best returned False')
            return False
        if self.data_ingestor.get_questions_best_is_max().count(question):
            self.app.logger.info('Method is_best returned True')
            return True
        self.app.logger.error('Method is_best returned Question not found')
        raise ValueError('Question not found')

    def states_mean(self, question):
        """
        Computes the mean of data values for each state for the given question.
        """
        self.app.logger.info('Entered method states_mean with parameter %s', question)
        result = self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values()\
                        .to_json()
        self.app.logger.info('Method states_mean returned: %s', result)
        return result

    def state_mean(self, question, state):
        """
        Computes the mean of data values for the specified state and question.
        """
        self.app.logger.info('Entered method state_mean with parameters %s, %s', question, state)
        data = self.question_data(question)
        result = data[data['LocationDesc'] == state]\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values()\
                        .to_json()
        self.app.logger.info('Method state_mean returned: %s', result)
        return result


    def best5(self, question):
        """
        Computes the top 5 states with the best data values for the given question.
        """
        self.app.logger.info('Entered method best5 with parameter %s', question)
        result = self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values(ascending=not self.is_best(question))\
                        .head(5)\
                            .to_json()
        self.app.logger.info('Method best5 returned: %s', result)
        return result

    def worst5(self, question):
        """
        Computes the top 5 states with the worst data values for the given question.
        """
        self.app.logger.info('Entered method worst5 with parameter %s', question)
        result = self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values(ascending=self.is_best(question))\
                        .head(5)\
                            .to_json()
        self.app.logger.info('Method worst5 returned: %s', result)
        return result

    def global_mean(self, question):
        """
        Computes the global mean of data values for the given question.
        """
        self.app.logger.info('Entered method global_mean with parameter %s', question)
        data = self.question_data(question)
        mean_value = data['Data_Value'].mean().item()
        result = json.dumps({"global_mean": mean_value})
        self.app.logger.info('Method global_mean returned: %s', result)
        return result

    def diff_from_mean(self, question):
        """
        Computes the difference of data values from the mean for each state.
        """
        self.app.logger.info('Entered method diff_from_mean with parameter %s', question)
        data = self.question_data(question)
        mean = data['Data_Value'].mean()

        data = data.groupby('LocationDesc')['Data_Value'].mean()
        result = (mean - data).to_json()
        self.app.logger.info('Method diff_from_mean returned: %s', result)
        return result

    def state_diff_from_mean(self, question, state):
        """
        Computes the difference of data values from the mean for the specified state.
        """
        self.app.logger.info('Entered method state_diff_from_mean with parameters %s, %s', \
            question, state)
        data = self.question_data(question)
        mean = data['Data_Value'].mean()

        data = data[data['LocationDesc'] == state]\
            .groupby('LocationDesc')['Data_Value']\
                .mean()

        result = (mean - data).to_json()
        self.app.logger.info('Method state_diff_from_mean returned: %s', result)
        return result

    def mean_by_category(self, question):
        """
        Computes the mean of data values for each category.
        """
        self.app.logger.info('Entered method mean_by_category with parameter %s', question)
        data = self.question_data(question)

        result = data.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])\
            ['Data_Value']\
                .mean()\
                    .to_json()
        self.app.logger.info('Method mean_by_category returned: %s', result)
        return result

    def state_mean_by_category(self, question, state):
        """
        Computes the mean of data values for each category for the specified state.
        """
        self.app.logger.info('Entered method state_mean_by_category with parameters %s, %s', \
            question, state)
        data = self.question_data(question)

        data = data[data['LocationDesc'] == state]\
            .groupby(['StratificationCategory1', 'Stratification1'])['Data_Value']\
                .mean()\
                    .to_json()
        with self.app.app_context():
            result = json.dumps({state: json.loads(data)})
            self.app.logger.info('Method state_mean_by_category returned: %s', result)
            return result

    def jobs(self):
        """
        Retrieves all the jobs in the task pool.
        """
        self.app.logger.info('Entered method jobs')
        result = []
        for task in self.app.tasks_runner.get_tasks():
            result.append({"job_id_" + str(task.job_id): task.status})

        with self.app.app_context():
            self.app.logger.info('Method jobs returned: %s', result)
            return result

    def num_jobs(self):
        """
        Retrieves the number of jobs in the task pool.
        """
        self.app.logger.info('Entered method num_jobs')
        self.app.logger.info('Method num_jobs returned: %s', len(self.app.tasks_runner.get_tasks()))
        return len(self.app.tasks_runner.get_tasks())
