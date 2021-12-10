import arxiv

def get_paper_data(paper_id):
    results = arxiv.query(query="",
                id_list=[paper_id],
                max_results=1)
    result = results[0]
    title, abstract = result['title'], result['summary']
    return title, abstract    