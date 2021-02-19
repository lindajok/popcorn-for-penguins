# This is a version of the Boolean search engine which only supports uppercase Boolean operators.

from sklearn.feature_extraction.text import CountVectorizer
import io
import re
import numpy as np
import enchant     


def prepare_data():
    """ Read a file and make a list of strings """
    documents = []
    article = ""
    f = io.open("data100.txt", mode="r", encoding="utf-8")
    for line in f:
        line = line.replace('\n', ' ')
        if line == "</article> ":
            clean = re.compile('<.*?>')
            clean_version = re.sub(clean, '', article)
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
terms2 = enchant.request_pwl_dict("data100_wordlist.txt")   
unknownword_list = []

# Make a file of list of words if file does not already exists in folder
f = open("data100_wordlist.txt", "w")
for k, v in t2i.items():
    f.write(k + "\n")
f.close()

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
        unknownword_list.append(t)
        return 'np.matrix(np.zeros(len(documents), dtype=int))'


def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())


def suggestions(w):
    """ Returns suggestions for similar words """
    suggested_wordlist = terms2.suggest(w)
    if suggested_wordlist:
        return "We didn't find anything matching \"{}\". Did you perhaps mean: {}?".format(w, '/'.join(word for word in suggested_wordlist))
    else:
        return "We didn't find anything matching \"{}\".".format(w)


def print_results(user_input):
    try:
        hits_matrix = eval(rewrite_query(user_input))
        hits_list = list(hits_matrix.nonzero()[1])
        print("Total number of matching documents: {:d}".format(len(hits_list)))

        for i, doc_idx in enumerate(hits_list):
            if i > 4:
                break
            else:
                print("Example of a matching doc #{:d}: {:s}...".format(i, documents[doc_idx][:50]))
    except:
        print("Wrong syntax. Please check that you use uppercase boolean operators (AND, OR, NOT)")

    global unknownword_list             # global variable needs to be decleared
    if unknownword_list:                # if there is unkown words
        for w in unknownword_list:
            print(suggestions(w))       # call function and print contents
    unknownword_list = []               # clear list 


def main():
    user_input = "0"
    while user_input != "":
        user_input = input("Write the query (press enter to stop): ") #.lower()
        try:
            if user_input == "":
                break
            else:
                print_results(user_input)
        except KeyError:
            print("Bad query")

main()
