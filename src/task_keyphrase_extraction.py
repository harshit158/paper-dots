import argparse

import fitz
from tqdm import tqdm
from PIL import Image

import config
import constituency_parser
from utils import search_and_annotate, read_file, get_block_containing_abstract
from extractor import extract_author, extract_year


def main(args):
    # Initializing Parser
    parser = constituency_parser.Parser()
    
    # Reading input and process the pages
    pages = read_file(args['filepath'])
    
    # Process each page
    for page in tqdm(pages):
        page_bbox = page.cropbox  # bounding box of full page
        text_blocks = page.get_text("blocks")
        
        # Text block containing the "Abstract"
        abstract_block = get_block_containing_abstract(text_blocks)
        
        x0, y0, x1, y1, text, abstract_block_no, block_type = abstract_block
        abstract_rect = [x0, y0, x1, y1]                     
        phrases = parser.parse(text)
        search_and_annotate(phrases, page, text_type='phrase', clip=abstract_rect)
        
        # Extracting and Highlighting author's email IDs        
        author_emails = extract_author(text_blocks[:abstract_block_no])
        clip=[0,0,page_bbox[2],abstract_rect[1]]
        search_and_annotate(author_emails, page, text_type='author', clip=clip, max_inst=1)
        
        # The year always appears in the last text block
        year=[extract_year(text_blocks[-1])]
        clip = text_blocks[-1][:4]
        search_and_annotate(year, page, text_type='year', clip=clip)
        
        if args.get('clip_abstract',False):
            # clip the area (only horizontally) that contains the just the abstract
            # from starting of page till the end of abstract 
            page.set_cropbox(fitz.Rect([0,0,page_bbox[2],y1+20]))
            zoom = 3    # zoom factor to increase resolution
            mat = fitz.Matrix(zoom, zoom)
            pix = page.getPixmap(matrix = mat)
            img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
        
            if args.get('save_abstract',False):
                pix.writeImage(config.ANNOTATED_FILEPATH+"abstract.png")
            
            return img    
        
        # Since we are interested only in highlighting "Abstract", we process just the "first page"
        # TODO: Process all the pages in a research paper
        break
    
    # save the annotated document
    # pages.save(config.ANNOTATED_FILEPATH+"annotated.pdf", garbage=4, deflate=True, clean=True)
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-fp', '--filepath',
                        type=str,
                        required=True,
                        help="Filepath - can be path on local disk or a URL")

    parser.add_argument('-ca', '--clip_abstract',
                        action='store_true',
                        default=True,
                        help='If true, clips and saves the annotated abstract as an image file')
    
    parser.add_argument('-sa', '--save_abstract',
                        action='store_true',
                        default=True,
                        help='If true, saves the annotated abstract')

    args = vars(parser.parse_args())
    
    main(args)