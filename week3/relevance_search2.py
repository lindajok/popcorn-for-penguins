from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import io
import numpy as np
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import re

'''
documents = []
while user_doc =! "":
    if user_doc == "":
        break
    else:
        documents.append(user_doc)
'''

title_list = []
f = io.open("data100.txt", mode="r", encoding="utf-8" )
for line in f:
    line = line.replace('\n', '')
    if "<article name=" in line:
        line = line.replace('<article name="', '')
        line = line.replace('">', '')
        title_list.append(line)
f.close()

separator = '\n'
titles = separator.join(title_list)

def prepare_data():
    documents = []
    article = ""
    f = io.open("data100.txt", mode="r", encoding="utf-8" )

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

body_list = prepare_data()
dictionary = {title_list[i]: body_list[i] for i in range(len(title_list))}

documents = prepare_data() # Documents in a list of strings format, left as a global variable

''' lemmatizing stuff

wnl = WordNetLemmatizer()
for words in documents:
    print(words + " ---> " + wnl.lemmatize(words))

lemmatizing stuff '''

tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
sparse_matrix = tfv5.fit_transform(documents).T.tocsr() # CSR: compressed sparse row format => order by terms

def print_results(user_input):
    query_vec5 = tfv5.transform([user_input]).tocsc()
    hits = np.dot(query_vec5, sparse_matrix)

    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
    print("\nAll given documents:\n\n{}".format(titles)) # prints the title of all articles, not a necessary function :D
    for score, i in ranked_scores_and_doc_ids:
        cut = documents[i]
        first_occurrence = documents[i].find(user_input)
        print("\nThe score of {} is {:.4f} in document: {:s}.\n...{:s}...\n".format(user_input, score, documents[i][:50], cut[first_occurrence:first_occurrence+200]))

#print(str(dictionary.keys()))

user_input = "0"
while user_input != "":
    user_input = input("Write the query (press enter to stop): ").lower()
    try:
        if user_input == "":
            break
        else:
            print_results(user_input)
    except KeyError:
        print("Bad query")
