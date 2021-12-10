import re

def extract_author(text_blocks):
    email_set = set()
    for block in text_blocks:
        x0,y0,x1,y1,text,_,_ = block

        # extract "cs.abc" from person1@cs.abc.edu
        emails_found=list(re.finditer('@(\w+\.)+[a-z]+', text))
        
        for email in emails_found:
            email=email.group()
            email_set.add(email[1:-4])
        
    return list(email_set)        

def extract_year(text_block):
    year_text = text_block[4].strip()
    search=re.search('(?<=[A-Z][a-z]{2}\s)\d+',year_text)
    if search:
        return search.group()
    return ''