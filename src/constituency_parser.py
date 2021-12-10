import re

from model_loader import Model

import utils
import config

model_path = config.CONSTITUENCY_PARSING['local_path']

class Parser(Model):
    def __init__(self):
        Model.__init__(self, model_path)
    
    def parse(self, sentence):
        # fetching model's output
        model_output=self.predict(sentence)

        # extracting noun chunks from the model's output
        raw_phrases = self.get_raw_noun_phrases(model_output)

        # cleaning raw_noun_phrases
        phrases = self.get_noun_phrases(raw_phrases)
        
        # final sanity check on phrases
        phrases = utils.sanitize_phrases(phrases)
        
        # TODO: filter the phrases - remove noisy phrases
        # phrases = self.filter_phrases(phrases)

        return phrases

    
    
    def get_noun_phrases(self, raw_noun_phrases):
        noun_phrases=[]
        for phrase in raw_noun_phrases:
            np=' '.join(re.findall(' [A-Za-z0-9\-]+(?=\))', phrase))
            noun_phrases.append(np)
        return noun_phrases

    def get_raw_noun_phrases(self, model_output):
        text=model_output['trees'].replace('NNP', '**')
        searches=re.finditer('\(NP \([^(NP)]+', text)            
        noun_phrases=[]                                                  
        for search in searches:
            start, end = search.span(0)[0], search.span(0)[1]            
            noun_phrases.append(self.parse_brackets(start, text))
        return noun_phrases
    
    def parse_brackets(self, start, result_text):
        arr=[]
        ptr=int(start)
        arr.append(result_text[ptr])
        ptr+=1
        while arr:
            #print(result_text[ptr])
            if result_text[ptr]==')':
                arr.pop(-1)
            elif result_text[ptr]=='(':
                arr.append(result_text[ptr])
                #print(arr)
            ptr+=1
        
        return result_text[start:ptr]

if __name__=="__main__":
    test_sentence="The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data."
    parser=Parser()
    output=parser.parse(test_sentence)
    print(output)