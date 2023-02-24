import tkinter as tk
from tkinter import filedialog, Text
from nltk.corpus import stopwords as dotw
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

root = tk.Tk()

# function to read the file and split sentences based on the full stop or other regex
def parse_doc(insource):
    source = open(insource, "r")
    sourced = source.readlines()
    article = sourced[0].split(". ")
    lines = []

    for line in article:
        # regex split based on a variety of characters
        lines.append(line.replace("[^a-zA-Z]", " ").split(" "))
    # pop the list to get the sentence
    lines.pop() 
    return lines

# function to check for the dotwords or commonly called stopwords
def line_similarity(l1, l2, dotw=None):
    if dotw is None:
        dotw = []
 
    l1 = [wembed.lower() for wembed in l1]
    l2 = [wembed.lower() for wembed in l2]
 
    complete_source = list(set(l1 + l2))

 # creating word vectors for the different senetences
    rdf1 = [0] * len(complete_source)
    rdf2 = [0] * len(complete_source)
 
   
    for wembed in l1:
        if wembed in dotw:
            continue
        rdf1[complete_source.index(wembed)] += 1
 
  
    for wembed in l2:
        if wembed in dotw:
            continue
        rdf2[complete_source.index(wembed)] += 1
 
    return 1 - cosine_distance(rdf1, rdf2)
 
# finding the cosine similarity of the sentences
def csmeasure(lines, sttokens):
    
    csmeasure1 = np.zeros((len(lines), len(lines)))
 
    for ptr1 in range(len(lines)):
        for ptr2 in range(len(lines)):
            if ptr1 == ptr2: 
                continue 
            csmeasure1[ptr1][ptr2] = line_similarity(lines[ptr1], lines[ptr2], sttokens)

    return csmeasure1

# function to create the summary after checking cosine similarity 
# sentences are ranked based on the similarity
def createshort(fileloc, top_n=5):
    sttokens = dotw.words('english')
    shorten = []
    lines = parse_doc(fileloc)
    line_csmeasure1 = csmeasure(lines, sttokens)
    lsgraph = nx.from_numpy_array(line_csmeasure1)
    scores = nx.pagerank(lsgraph)

# sorting based on rank of the graph and choosing the sentences
    superiority = sorted(((scores[i],s) for i,s in enumerate(lines)), reverse=True)
    for i in range(top_n):
        shorten.append(" ".join(superiority[i][1]))

    print("FINAL TEXT: \n", ". ".join(shorten))

# tkinter implementation for the text summarizer

def add_source():
    fileloc = filedialog.askopenfilename(initialdir="/", title="Select source", filetypes=(("Text sources", "*.txt"),))
    print(fileloc)
    createshort(fileloc)

canvas = tk.Canvas(root, height=500, width=500, bg="#263D42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

open_source = tk.Button(root, text="Open source", padx=10, pady=5, fg="white", bg="#263D42", command=add_source)
open_source.pack()
summary_label = tk.Label(frame, text="Summary will appear here", bg="white")
summary_label.pack()

root.mainloop()