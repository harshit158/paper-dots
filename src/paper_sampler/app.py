from flask import Flask, request
from paper_sampler import Sample
from utils import get_paper_data


flask_app = Flask(__name__)
sample = Sample()

@flask_app.route('/', methods=['GET'])
def index_page():
    paper_text = request.args.get('text')
    return paper_text

@flask_app.route('/nextpaper',methods=['GET'])
def get_next_paper():
    paper_id = request.args.get('paper_id')
    title, abstract = get_paper_data(paper_id)
    next_paper_id = sample.sample(paper_id, title, abstract)
    return next_paper_id

@flask_app.route('/encode',methods=['GET'])
def encode():
    pass

if __name__=='__main__':
    flask_app.run(host ='0.0.0.0',port=8080, debug=True)