from flask import Flask, render_template, request
import io
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re
import numpy as np
from datetime import datetime
# from nltk.stem import PorterStemmer
# from nltk.tokenize import sent_tokenize, word_tokenize
# import copy

#Initialize Flask instance
app = Flask(__name__)


def prepare_data():
    """ Read a file and make a list of strings """
    documents = []
    article = ""
    f = io.open("static/data100.txt", mode="r", encoding="utf-8")
    for line in f:
        line = line.replace('\n', ' ')
        if line == "</article> ":
            clean_version = re.sub("</article>", '', article)
            documents.append(clean_version)
            article=""
        else:
            article+=line
    f.close()
    return documents


documents = prepare_data()
cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'(?u)\b\w+\b')
sparse_matrix = cv.fit_transform(documents)
dense_matrix = sparse_matrix.todense()
td_matrix = dense_matrix.T
sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_ # dictionary of terms
terms = cv.get_feature_names()

tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r'(?u)\b\w+\b')
sparse_matrix = tfv5.fit_transform(documents).T.tocsr()


def rewrite_token(t):
    d = {"AND": "&",
     "OR": "|",
     "NOT": "1 -",
     "(": "(", ")": ")"}
    if t in d:
        return d.get(t)
    elif t.lower() in terms:
        return 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t.lower())
    else:
        return 'np.matrix(np.zeros(len(documents), dtype=int))'


def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())


def format(user_input):
    matches = []
    dict = {}
    hits_matrix = eval(rewrite_query(user_input))
    hits_list = list(hits_matrix.nonzero()[1])
    for i, doc_idx in enumerate(hits_list):
        title = re.sub(r'<article name="', '', documents[doc_idx])
        title = re.sub('">.*', '', title)
        content = re.sub('<.*?>', '', documents[doc_idx])
        dict[title]=content
        matches.append(dict)  
    return matches


#Function search() is associated with the address base URL + "/search"
@app.route('/search', methods=['GET', 'POST'])
def search():
    today = datetime.today()
    day_name = today.strftime("%A")

    mealtypes = ['-', 'Starter', 'Main', 'Dessert']

    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches = []

    #If query exists (i.e. is not None)
    if query:
        matches = format(query)

    #Render index.html with matches variable
    return render_template('index.html', matches=matches, day=day_name, mealtypes=mealtypes)