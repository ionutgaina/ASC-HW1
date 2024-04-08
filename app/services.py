class TaskService:
    
    def __init__(self, data_ingestor):
        self.data_ingestor = data_ingestor
        
    def question_data(self, question):
        data = self.data_ingestor.data
        data = data[data['Question'] == question]
        
        return data
    
    def is_best(self, question):
        if self.data_ingestor.questions_best_is_min.count(question):
            return False
        elif self.data_ingestor.questions_best_is_max.count(question):
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
        return data['Data_Value'].mean()\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .to_json()
    
        
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