from flask import Flask, render_template, request
import io
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re
import numpy as np
from datetime import datetime
from nltk.stem import PorterStemmer
import nltk
from copy import deepcopy
# from nltk.tokenize import sent_tokenize, word_tokenize
stemmer = PorterStemmer()

#Initialize Flask instance
app = Flask(__name__)

def titles():
    f = io.open('static/titles.txt', mode='r', encoding='UTF-8')
    for line in f:
        line = line.split('*')
    f.close()
    return line


def ingredients():
    f = io.open('static/ingredients.txt', mode='r', encoding='UTF-8')
    for line in f:
        line = line.split('@')
    f.close()
    return line


def methods():
    f = io.open('static/methods.txt', mode='r', encoding='UTF-8')
    for line in f:
        line = line.split('@')
    f.close()
    return line


def stem(lst): 
    for i in range(len(lst)):
        words = nltk.word_tokenize(lst[i]) 
        words = [stemmer.stem(word) for word in words]                        
        lst[i] = ' '.join(words)
    return lst


documents = prepare_recipes()
ingredients(documents)
copy_documents = deepcopy(documents)
stemmed_documents = (stem(copy_documents))

cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'(?u)\b\w+\b')
sparse_matrix = cv.fit_transform(stemmed_documents)
dense_matrix = sparse_matrix.todense()
td_matrix = dense_matrix.T
sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_ 
terms = cv.get_feature_names()

tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r'(?u)\b\w+\b')
sparse_matrix = tfv5.fit_transform(documents).T.tocsr()


def stem_query(query):
    boolean = ["AND", "OR", "NOT", "(", ")"]
    for word in query.split():
        if word not in boolean:
            stemmed = stemmer.stem(word)
            query = re.sub(word, stemmed, query)
    return query


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


def get_content(doc_idx):
    return re.sub('<.*?>', '', documents[doc_idx])
    
    
def get_title(doc_idx):
    title = re.sub(r'<article name="', '', documents[doc_idx])
    title = re.sub('">.*', '', title)
    return title


def format(hits):
    recipes = []
    recipe = {}
    for i, doc_idx in enumerate(hits):
        title = get_title(doc_idx)
        content = get_content(doc_idx)
        recipe[title]=content
        recipes.append(recipe)  
    return recipes


def get_matches(user_input):
    hits_matrix = eval(rewrite_query(user_input))
    hits_list = list(hits_matrix.nonzero()[1])
    return format(hits_list)


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
        query = stem_query(query)
        matches = get_matches(query)

    #Render index.html with matches variable
    return render_template('index.html', matches=matches, day=day_name, mealtypes=mealtypes)
