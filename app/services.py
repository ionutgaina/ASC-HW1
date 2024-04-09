from flask import json

class TaskService:
    
    def __init__(self, data_ingestor, app=None):
        self.data_ingestor = data_ingestor
        self.app = app
        
    def question_data(self, question):
        data = self.data_ingestor.get_data()
        data = data[data['Question'] == question]
        
        return data
    
    def is_best(self, question):
        if self.data_ingestor.get_questions_best_is_min().count(question):
            return False
        elif self.data_ingestor.get_questions_best_is_max().count(question):
            return True
        else:
            raise ValueError('Question not found')
    
    def states_mean(self, question):
        
        return self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values()\
                        .to_json()
                        
    def state_mean(self, question, state):
        data = self.question_data(question)
        return data[data['LocationDesc'] == state]\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values()\
                        .to_json()
                        
    def best5(self, question):
        return self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values(ascending=not self.is_best(question))\
                        .head(5)\
                            .to_json()
                            
    def worst5(self, question):
        return self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values(ascending=self.is_best(question))\
                        .head(5)\
                            .to_json()
                            
    def global_mean(self, question):
        data = self.question_data(question)
        mean_value = data['Data_Value'].mean().item()
        return json.dumps({"global_mean": mean_value})
    
        
    def diff_from_mean(self, question):
        data = self.question_data(question)
        mean = data['Data_Value'].mean()
        
        data = data.groupby('LocationDesc')['Data_Value'].mean()
        return (mean - data).to_json()

    def state_diff_from_mean(self, question, state):
        data = self.question_data(question)
        mean = data['Data_Value'].mean()
        
        data = data[data['LocationDesc'] == state]\
            .groupby('LocationDesc')['Data_Value']\
                .mean()
                
        return (mean - data).to_json()
    
    def mean_by_category(self, question):  
        data = self.question_data(question)
        
        return data.groupby(['LocationDesc', 'StratificationCategory1', 'Stratification1'])['Data_Value']\
            .mean()\
                .to_json()
                
    def state_mean_by_category(self, question, state):
        data = self.question_data(question)

        data = data[data['LocationDesc'] == state]\
            .groupby(['StratificationCategory1', 'Stratification1'])['Data_Value']\
                .mean()\
                    .to_json()
        with self.app.app_context():
            return json.dumps({state : json.loads(data)})
        
    
    def jobs(self):
        result = []
        for task in self.app.tasks_runner.get_tasks():
            result.append({"job_id_" + str(task.job_id): task.status})
            
        with self.app.app_context():
            return result
        
    def num_jobs(self):
        return len(self.app.tasks_runner.get_tasks())