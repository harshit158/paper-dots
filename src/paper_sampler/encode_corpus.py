import pandas as pd
df=pd.read_json('/home/hs/Downloads/arxiv-metadata-oai-snapshot.json', lines=True,
                dtype = {"id": object})

def clean_text(text):
    text=re.sub('\n', ' ', text)
    text=re.sub(r'\s+', ' ', text)
    return text

id2text = {}
for _,row in df.iterrows():
    abstract_plus_title = row['abstract']+' '+row['title']
    abstract_plus_title = clean_text(abstract_plus_title)
    id2text[row['id']] = abstract_plus_title
    
ids = id2text.keys()
paper_texts = list(id2text.values())
corpus_embeddings = model.encode(paper_texts, convert_to_tensor=True)

# saving embeddings to a file
import h5py
with h5py.File('corpus_embeddings.hdf5', 'w') as f:
    dset = f.create_dataset("corpus_embeddings", data=corpus_embeddings)

# saving corresponding ids to a file
import pickle
with open('corpus_ids.pkl', 'wb') as f:
    pickle.dump(list(ids), f)