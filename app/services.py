class TaskService:
    
    def __init__(self, data_ingestor):
        self.data_ingestor = data_ingestor
        
    def question_data(self, question):
        data = self.data_ingestor.data
        data = data[data['Question'] == question]
        
        return data
    
    def states_mean(self, question):
        
        return self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values()\
                        .to_json()
        
    def diff_from_mean(self, question):
        
        data = self.question_data(question)\
            .groupby('LocationDesc')['Data_Value']\
                .mean()\
                    .sort_values()

        mean = data.mean()
        return (abs(data - mean)).to_json()