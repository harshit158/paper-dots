from allennlp.predictors.predictor import Predictor

class Model():
    def __init__(self, model_path):
        '''Initializes the predictor from AllenNLP'''
        self.predictor = Predictor.from_path(model_path)
    
    def predict(self, sentence):
        model_output=self.predictor.predict(sentence)
        return model_output