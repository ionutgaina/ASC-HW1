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
        data = self.data_ingestor.get_data()
        data = data[data['Question'] == question]
        return data

    def is_best(self, question):
        """
        Checks if the given question is best when the value is maximum.
        """
        if self.data_ingestor.get_questions_best_is_min().count(question):
            return False
        if self.data_ingestor.get_questions_best_is_max().count(question):
            return True
        raise ValueError('Question not found')

    def states_mean(self, question):
        """
        Computes the mean of data values for each state for the given question.
        """
        return self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values()\
                        .to_json()

    def state_mean(self, question, state):
        """
        Computes the mean of data values for the specified state and question.
        """
        data = self.question_data(question)
        return data[data['LocationDesc'] == state]\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values()\
                        .to_json()

    def best5(self, question):
        """
        Computes the top 5 states with the best data values for the given question.
        """
        return self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values(ascending=not self.is_best(question))\
                        .head(5)\
                            .to_json()

    def worst5(self, question):
        """
        Computes the top 5 states with the worst data values for the given question.
        """
        return self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values(ascending=self.is_best(question))\
                        .head(5)\
                            .to_json()

    def global_mean(self, question):
        """
        Computes the global mean of data values for the given question.
        """
        data = self.question_data(question)
        mean_value = data['Data_Value'].mean().item()
        return json.dumps({"global_mean": mean_value})

    def diff_from_mean(self, question):
        """
        Computes the difference of data values from the mean for each state.
        """
        data = self.question_data(question)
        mean = data['Data_Value'].mean()

        data = data.groupby('LocationDesc')['Data_Value'].mean()
        return (mean - data).to_json()

    def state_diff_from_mean(self, question, state):
        """
        Computes the difference of data values from the mean for the specified state.
        """
        data = self.question_data(question)
        mean = data['Data_Value'].mean()

        data = data[data['LocationDesc'] == state]\
            .groupby('LocationDesc')['Data_Value']\
                .mean()

        return (mean - data).to_json()

    def mean_by_category(self, question):
        """
        Computes the mean of data values for each category.
        """
        data = self.question_data(question)

        return data.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])\
            ['Data_Value']\
                .mean()\
                    .to_json()

    def state_mean_by_category(self, question, state):
        """
        Computes the mean of data values for each category for the specified state.
        """
        data = self.question_data(question)

        data = data[data['LocationDesc'] == state]\
            .groupby(['StratificationCategory1', 'Stratification1'])['Data_Value']\
                .mean()\
                    .to_json()
        with self.app.app_context():
            return json.dumps({state: json.loads(data)})

    def jobs(self):
        """
        Retrieves all the jobs in the task pool.
        """
        result = []
        for task in self.app.tasks_runner.get_tasks():
            result.append({"job_id_" + str(task.job_id): task.status})

        with self.app.app_context():
            return result

    def num_jobs(self):
        """
        Retrieves the number of jobs in the task pool.
        """
        return len(self.app.tasks_runner.get_tasks())
