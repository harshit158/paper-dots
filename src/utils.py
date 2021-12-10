from IPython.core.display import display, HTML
import re
import io
import fitz
import urllib.request, urllib.parse, urllib.error
import requests
from requests.models import Response
import config
import pytz
from datetime import datetime

def render(cleaned_spans, tok_tags, colour='yellow', debug=False):
    html_string_components = []
    flat_spans = sum(cleaned_spans, [])
    
    extra_info = '<sup style="background-color:yellow">{}</sup>' if debug else ''

    for idx, tok in enumerate(tok_tags):
        if idx not in flat_spans:
            html_string_components.append(str(tok[0])+extra_info.format(tok[1]))
        else:
            html_string_components.append(f'<span style="background-color:{colour}">{tok[0]}</span>'+extra_info.format(tok[1]))

    html_to_render = '<p> '+' '.join(html_string_components) + ' </p>'
    display(HTML(html_to_render))

def search_and_annotate(phrases, page, text_type, clip=None, max_inst=None):
    """Searches and annotates the found object

    Args:
        phrases (List): [description]
        page ([type]): [description]
        clip (List of coordinates, optional): The area within which to search text. Defaults to None.
        max_inst (int, optional): Number of found instances to highlight. Defaults to None.
    """
    # update annotation according to text_type
    # (page.addHighlightAnnot()).setColors(config.ANNOT_COLOURS[text_type])
    for phrase in phrases:
        text_instances = page.searchFor(phrase)
        if not text_instances:
            continue
        text_instances = text_instances[:max_inst] if max_inst else text_instances
        for inst in text_instances:
            if clip and (inst[0]<clip[0] or inst[1]<clip[1] or inst[2]>clip[2] or inst[3]>clip[3]):
                continue
            highlight=page.addHighlightAnnot(inst)        # highlight the found text
            
            # TODO: annotate based on the type/importance of phrase
            highlight.setColors(config.ANNOT_COLOURS[text_type])
            highlight.update()

def sanitize_phrases(phrases):
    for idx, phrase in enumerate(phrases):
        phrase = re.sub('\s*\-\s*', '', phrase) # "represent- ation model" -> "representation model"
        phrase = phrase.strip()                 # remove spaces from end 
        phrases[idx] = phrase
    
    phrases = [x for x in phrases if x]         # discard empty phrases
    return phrases

def compose_paper_url(paper_id):
    filepath =  f'https://arxiv.org/pdf/{paper_id}.pdf'
    return filepath

def read_file(filepath):
    if filepath.startswith('https'):
        if not filepath.endswith('pdf'):
            # if not a pdf link, process and convert the url to point to pdf url
            paper_id = filepath.split('/')[-1]
            filepath = compose_paper_url(paper_id)
            
        pdf_stream = urllib.request.urlopen(filepath).read()
        pages = fitz.open(stream=pdf_stream, filetype='pdf')
    else:
        pages = fitz.open(filepath)
    
    return pages

def get_block_containing_abstract(text_blocks):
    '''Finds the text block that contains the abstract'''
    for block in text_blocks:
        x0, y0, x1, y1, text, block_no, block_type = block
        text = text.strip().lower()
        if re.search('abstract', text.strip().lower()):
            if text.endswith('abstract'): 
                return text_blocks[block_no+1]
            else:
                return text_blocks[block_no]


def get_current_time(tz='America/New_York'):
    """Returns time zone

    Args:
        tz (str, optional): . Defaults to 'America/New_York'.

    Returns:
        str : Current time as per the time zone
    """
    tz=pytz.timezone(tz)
    dt=datetime.now(tz)
    return dt.isoformat()

def sample_next_paper(paper_id):
    URL = "http://localhost:8080/nextpaper"
    PARAMS = {'paper_id':paper_id} 
    response = requests.get(url = URL, params = PARAMS)
    result = response.content
    result = result.decode() # converting bytes to string
    return result

def get_binary_img(image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr