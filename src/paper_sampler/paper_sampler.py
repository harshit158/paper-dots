import pandas as pd
import h5py
from sentence_transformers import SentenceTransformer, util
import re
import pickle


class Sample():
    """Samples a relevant paper given an input, using corpus_embeddings
    """
    
    def __init__(self):
        # Reading corpus_embeddings
        data=h5py.File('./data/corpus_embeddings.hdf5', 'r')
        self.corpus_embeddings=data['corpus_embeddings'][()]
        
        # Reading corpus ids
        self.corpus_ids = pickle.load(open('./data/corpus_ids.pkl','rb'))
        
        assert len(self.corpus_embeddings)==len(self.corpus_ids), '# of corpus ids != # of corpus embeddings'
        
        # Loading model to encode input text
        self.model = SentenceTransformer('allenai-specter')
    
    def clean_text(self, text):
        text=re.sub('\n', ' ', text)
        text=re.sub(r'\s+', ' ', text)
        return text

    def sample(self, paper_id, abstract, title):
        """Given paper_text ( = paper_abstract+paper_title), samples out the most relevant paper

        Args:
            paper_id (str): the arxiv id of the paper which is treated as the starting point
            abstract (str): abstract of paper
            title (str)   : title of paper

        Returns:
            [type]: [description]
        """
        paper_text = abstract + ' ' + title
        paper_text = self.clean_text(paper_text)
        
        # get the vector for query paper
        query_embedding = self.model.encode(paper_text, convert_to_tensor=True)

        # retrieve top similar papers
        search_hits = util.semantic_search(query_embedding, self.corpus_embeddings)[0]
        
        # do softmax normalization and sampling using random strategy
        next_paper_id = self.corpus_ids[search_hits[0]['corpus_id']]
        
        if next_paper_id == paper_id:
            next_paper_id = self.corpus_ids[search_hits[1]['corpus_id']]
        
        return str(next_paper_id)
        


if __name__=='__main__':
    paper_id = '0704.0001'
    title = "Calculation of prompt diphoton production cross sections at Tevatron and LHC energies"
    abstract = '''A fully differential calculation in perturbative quantum chromodynamics is presented for 
                the production of massive photon pairs at hadron colliders. All next-to-leading order perturbative 
                contributions from quark-antiquark, gluon-(anti)quark, and gluon-gluon subprocesses are included, 
                as well as all-orders resummation of initial-state gluon radiation valid at next-to-next-to-leading 
                logarithmic accuracy. The region of phase space is specified in which the calculation is most reliable. 
                Good agreement is demonstrated with data from the Fermilab Tevatron, and predictions are made for more 
                detailed tests with CDF and DO data. Predictions are shown for distributions of diphoton pairs produced 
                at the energy of the Large Hadron Collider (LHC). Distributions of the diphoton pairs from the decay of
                a Higgs boson are contrasted with those produced from QCD processes at the LHC, showing that enhanced 
                sensitivity to the signal can be obtained with judicious selection of events.'''
    
    sample = Sample()
    result = sample.sample(paper_id, abstract, title)
    print(result)