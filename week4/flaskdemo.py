from flask import Flask, render_template, request
import io

from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import copy

#Initialize Flask instance
app = Flask(__name__)

def prepare_data():
    """ Read a file and make a list of strings """
    documents = []
    article = ""
    f = io.open("static/gutenberg.txt", mode="r", encoding="utf-8" )

    for line in f:
        line = line.replace('\n', ' ')
        if line == "</article> ":
                clean_version = BeautifulSoup(article, "html.parser").text
                documents.append(clean_version)
                article=""
        else:
                article+=line

    f.close()

    return documents

documents = prepare_data()

#Function search() is associated with the address base URL + "/search"
@app.route('/search')
def search():
    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []

    #If query exists (i.e. is not None)
    if query:
        #Look at each entry in the example data
        for entry in documents:
            #If an entry name contains the query, add the entry to matches
            if query.lower() in entry.lower():
                matches.append(entry)

    #Render index.html with matches variable
    return render_template('index.html', matches=matches)
