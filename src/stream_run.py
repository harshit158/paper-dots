#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 19:02:23 2021

@author: prashank
"""

import streamlit as st
from PIL import Image
import streamlit.components.v1 as components

import codecs

import task_keyphrase_extraction, task_knowledge_graph


img = Image.open("logo.png")

st.image(img, width=500)

url = st.text_input('Enter the paper URL here ...')

if url:
    annotated_img=task_keyphrase_extraction.main({"filepath":url,
                                                "clip_abstract":True,
                                                "save_abstract":True})
    st.image(annotated_img, width=1000)

    if st.button('Knowledge Graph'):
        
        task_knowledge_graph.main({"filepath":url})

footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by <a style='display: block; text-align: center;' href="" target="_blank">Harshit Sharma</a> <a style='display: block; text-align: center;' href="https://prashankkadam.github.io/" target="_blank">Prashank Kadam</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)

# st.sidebar.image(img)

# # original_title = '<p style="font-family:Courier; color:Blue; font-size: 20px;">Original image</p>'

# url = st.sidebar.text_input('Enter the paper URL here ...')

# side_menu_selectbox = st.sidebar.radio('Select ...',('Annotations', 'Knowledge Graphs'))

# def annotations():
#     # st.write("This is the annotations page")
#     if url:
#         annotated_img=task_keyphrase_extraction.main({"filepath":url,
#                                     "clip_abstract":True,
#                                     "save_abstract":True})
#         st.image(annotated_img, width=1000)

# def knowledge_graphs():
#     # st.write("This is the knowledge graphs page")
#     if url:
#         task_knowledge_graph.main({"filepath":url})
#         HtmlFile = open('../output/graph.html', 'r', encoding='utf-8')
#         # source_code = HtmlFile.read() 
#         # components.iframe(width=2000)
        
#         # bootstrap 4 collapse example
#         components.html(
#             """
#             <html>
#             <head>
#             <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.16.1/vis-network.min.js"> </script>
#             <center>
#             <h1></h1>
#             </center>

#             </head>

#             <body>
#             <div id = "mynetwork"></div>


#             <script type="text/javascript">

#                 // initialize global variables.
#                 var edges;
#                 var nodes;
#                 var network; 
#                 var container;
#                 var options, data;

                
#                 // This method is responsible for drawing the graph, returns the drawn network
#                 function drawGraph() {
#                     var container = document.getElementById('mynetwork');
                    
                    

#                     // parsing and collecting nodes and edges from the python
#                     nodes = new vis.DataSet([{"id": " we", "label": " we", "shape": "dot"}, {"id": " English , which multiplies the available data to train acoustic models in comparison with TED - LIUM 2 , by a factor of more than two", "label": " English , which multiplies the available data to train acoustic models in comparison with TED - LIUM 2 , by a factor of more than two", "shape": "dot"}, {"id": " ded-", "label": " ded-", "shape": "dot"}, {"id": " to speech recognition in English", "label": " to speech recognition in English", "shape": "dot"}, {"id": " which", "label": " which", "shape": "dot"}, {"id": " the available data", "label": " the available data", "shape": "dot"}, {"id": " We", "label": " We", "shape": "dot"}, {"id": " the recent development on Auto- matic Speech Recognition ( ASR ) systems", "label": " the recent development on Auto- matic Speech Recognition ( ASR ) systems", "shape": "dot"}, {"id": " of the TED - LIUM release 3 corpus", "label": " of the TED - LIUM release 3 corpus", "shape": "dot"}, {"id": " HMM", "label": " HMM", "shape": "dot"}, {"id": " state - of - the - art", "label": " state - of - the - art", "shape": "dot"}, {"id": " the HMM- based ASR system", "label": " the HMM- based ASR system", "shape": "dot"}, {"id": " the end - to - end ASR system", "label": " the end - to - end ASR system", "shape": "dot"}, {"id": " two repar- titions of the TED - LIUM release 3 corpus", "label": " two repar- titions of the TED - LIUM release 3 corpus", "shape": "dot"}]);
#                     edges = new vis.DataSet([{"from": " we", "label": " present", "to": " English , which multiplies the available data to train acoustic models in comparison with TED - LIUM 2 , by a factor of more than two"}, {"from": " ded-", "label": " icated", "to": " to speech recognition in English"}, {"from": " which", "label": " multiplies  in comparison with TED - LIUM 2", "to": " the available data"}, {"from": " We", "label": " present  in comparison with the two previous releases of the TED - LIUM Corpus from 2012 and 2014", "to": " the recent development on Auto- matic Speech Recognition ( ASR ) systems"}, {"from": " We", "label": " demonstrate", "to": " of the TED - LIUM release 3 corpus"}, {"from": " HMM", "label": " based", "to": " state - of - the - art"}, {"from": " the HMM- based ASR system", "label": " outperforms", "to": " the end - to - end ASR system"}, {"from": " we", "label": " propose", "to": " two repar- titions of the TED - LIUM release 3 corpus"}]);

#                     // adding nodes and edges to the graph
#                     data = {nodes: nodes, edges: edges};

#                     var options = {
#                 "configure": {
#                     "enabled": false
#                 },
#                 "edges": {
#                     "color": {
#                         "inherit": true
#                     },
#                     "smooth": {
#                         "enabled": false,
#                         "type": "continuous"
#                     }
#                 },
#                 "interaction": {
#                     "dragNodes": true,
#                     "hideEdgesOnDrag": false,
#                     "hideNodesOnDrag": false
#                 },
#                 "physics": {
#                     "enabled": true,
#                     "stabilization": {
#                         "enabled": true,
#                         "fit": true,
#                         "iterations": 1000,
#                         "onlyDynamicEdges": false,
#                         "updateInterval": 50
#                     }
#                 }
#             };
                    
                    

                    

#                     network = new vis.Network(container, data, options);
                
                    


                    

#                     return network;

#                 }

#                 drawGraph();

#             </script>
#             </body>
#             </html>
#             """,
#             height=1500,
#             width=1500
#         )
        

# if side_menu_selectbox == 'Annotations':
#         annotations()
# elif side_menu_selectbox == 'Knowledge Graphs':
#         knowledge_graphs()
        