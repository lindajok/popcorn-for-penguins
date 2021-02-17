# This is a version of the Boolean search engine which only supports uppercase Boolean operators.

from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import io

def prepare_data():
    """ Read a file and make a list of strings """
    documents = []
    article = ""
    f = io.open("data100.txt", mode="r", encoding="utf-8" )                 # Change the name if you want to change the dataset 
    for line in f:
        line = line.replace('\n', ' ')                                      # Replace newline characers with space
        if line == "</article> ":                                           # Locate boundaries between articles
                clean_version = BeautifulSoup(article, "html.parser").text  # Remove tags
                documents.append(clean_version)                             # Add the article string without tags to the list of documents
                article=""                                                  # Define "auxiliary" variable again
        else:
                article+=line                                                                        
    f.close()
    return documents


documents = prepare_data() # Documents in a list of strings format, left as a global variable

cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'(?u)\b\w+\b')
sparse_matrix = cv.fit_transform(documents)
dense_matrix = sparse_matrix.todense()
td_matrix = dense_matrix.T
sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_ # dictionary of terms

def rewrite_token(t):
    d = {"AND": "&",
     "OR": "|",
     "NOT": "1 -",
     "(": "(", ")": ")"}
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

def input_string(user_input): # tool for handling unknown terms
    string = user_input
    string = string.replace(' AND ', ' ')
    string = string.replace(' OR ', ' ')
    string = string.replace('NOT ', '')
    string = string.replace(' NOT ', ' ')
    li = string.split(' ')
    return li

def print_results(user_input):
    for i in input_string(user_input): # PRINTING
        if i not in t2i: # IF TERM
            print("Given term '{}' not found in any document.".format(i)) # NOT FOUND
    hits_matrix = eval(rewrite_query(user_input))
    hits_list = list(hits_matrix.nonzero()[1])
    print("Total number of matching documents: {:d}".format(len(hits_list)))
    for i, doc_idx in enumerate(hits_list):
        if i > 4:
            break
        else:
            print("Example of a matching doc #{:d}: {:s}...".format(i, documents[doc_idx][:50]))

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
