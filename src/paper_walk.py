'''
This module is executed by Airflow in a set interval ("Daily" by default)
Each execution performs one-step walk over the paper-space
1. Fetch latest record from db for a user
2. Run Analysis on top of that
3. Mail Delivery
4. Sample next paper and store it in DB
'''

import argparse
import os

import logging
log = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)

import information_extraction
from mongo_utils import MongoUtils
from dotenv import load_dotenv; load_dotenv()
from mail_sender import send_mail
from utils import get_current_time, sample_next_paper, compose_paper_url, get_binary_img

# Loading environment variables
USER_EMAIL = os.getenv('USER_EMAIL')

# Initializing Mongo connection
mongo_obj = MongoUtils(db='paper_dots')

def walk():
    """Performs one cycle in the pipeline"""
    
    # 1. Fetch most recent record for the intended user (which is also the paper-to-read)
    print(f'Fetching paper-to-read for {USER_EMAIL}')
    paper_to_read = mongo_obj.get_recent(USER_EMAIL)
    paper_id = paper_to_read['paper_id']
    print(f'Found paper_id {paper_id}')
    
    # 2. Run analysis on paper_to_read (last record from db)
    paper_url = compose_paper_url(paper_id)
    print(paper_url)
    deliverables = information_extraction.main({"filepath":paper_url, 
                                                "ke":True, 
                                                "showke":True,
                                                "clip_abstract":True})
    print('Analysis done')
    
    # 3. Deliver mail containing analysis results
    img = deliverables['ke']
    img_binary = get_binary_img(img)
    send_mail('harshit158@gmail.com', book_image=img_binary)
    
    # 4. Sample next paper
    next_paper_id = sample_next_paper(paper_id)
    print('Next paper_id {}'.format(next_paper_id))
    
    # 5. Store the next paper-to-read in database
    doc = {'paper_id':next_paper_id,
           'date':get_current_time()}
    mongo_obj.push(USER_EMAIL, doc)


if __name__=="__main__":
    parser = argparse.ArgumentParser()    
    
    parser.add_argument('-r', '--reset',
                        action='store_true',
                        default=False,
                        help="If True, inserts the seed paper data in the db")
    
    args = vars(parser.parse_args())
    
    if args['reset']:
        # Reset the data in mongodb
        mongo_obj.push('harshit158@gmail.com', doc = {'paper_id':'1810.04805','date':get_current_time()})
    
    walk()