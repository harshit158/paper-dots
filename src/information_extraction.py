import argparse

# importing individual tasks
import task_keyphrase_extraction
#import task_knowledge_graph

def main(args):

    if not args.get('kg') and not args.get('ke'):
        print('None tasks selected')
    
    deliverables = {}
    
    # Task: Build Knowledge Graph
    if args.get('kg'):
        # task_knowledge_graph.main()
        pass
        
    # Task: Keyphrase Extraction
    if args.get('ke'):
        abstract_img = task_keyphrase_extraction.main(args)
        
        if args.get('showke'):
            abstract_img.show()
        deliverables['ke']=abstract_img
        
    return deliverables
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-kg', '--kg',
                        action='store_true',
                        default=True,
                        help='If true, builds Knowledge Graph')
    
    parser.add_argument('-ke', '--ke',
                        action='store_true',
                        default=True,
                        help='If true, performs Keyphrase Extraction')
    
    parser.add_argument('-showke',
                        action='store_true',
                        default=False,
                        help='If true, displays the annotated image from console')
    
    parser.add_argument('-fp', '--filepath',
                        type=str,
                        required=True,
                        help="Filepath - can be path on local disk or a URL")

    parser.add_argument('-ca', '--clip_abstract',
                        action='store_true',
                        default=True,
                        help='If true, clips and saves the annotated abstract as an image file')

    args = vars(parser.parse_args())
    
    main(args)