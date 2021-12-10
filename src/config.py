# Input paths for pretrained models
CONSTITUENCY_PARSING = {
    'web_path'  : "https://storage.googleapis.com/allennlp-public-models/elmo-constituency-parser-2020.02.10.tar.gz",
    'local_path': '../pretrained_weights/elmo-constituency-parser-2020.02.10.tar.gz'
}

OPENIE = {
    'web_path'  : "https://storage.googleapis.com/allennlp-public-models/openie-model.2020.03.26.tar.gz",
    'local_path': '../pretrained_weights/openie-model.2020.03.26.tar.gz'
}

# location to store annotated PDF
ANNOTATED_FILEPATH = '../output/'

# annotation properties for different types of entities
ANNOT_COLOURS = {
    "author": {"stroke":(153/255, 153/255, 255/255)}, # green
    "phrase": {"stroke":(255/255, 255/255, 0/255)},   # yellow
    "year"  : {"stroke":(255/255, 153/255, 153/255)}  # yellow
}