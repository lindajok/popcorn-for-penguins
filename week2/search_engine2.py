from sklearn.feature_extraction.text import CountVectorizer
from bs4 import BeautifulSoup
import io

def prepare_data():
    """ Read a file and make a list of strings """
    
    documents = []
    article = ""
    f = io.open("data100.txt", mode="r", encoding="utf-8" )    # Change the name if you want to test with the 1000 article file
    
    for line in f:
        line = line.replace('\n', ' ')                                      # Replace newline characers with space (have to add a space, otherwise it
                                                                                    # will parse wrong [heading and first word of a paragpraph will
                                                                                    # join together]. Other solution?)
        if line == "</article> ":                                           # Locate boundaries between articles
                clean_version = BeautifulSoup(article, "html.parser").text  # Remove tags
                documents.append(clean_version)                             # Add the article string without tags to the list of documents
                article=""                                                  # Define "auxiliary" variable again
        else:
                article+=line                                                                        
    
    f.close()
    
    return documents

documents = prepare_data() # Documents in a list of strings format, left as a global variable

# This is the code we had earlier -->
# We could eventually put it into a function too
cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'(?u)\b\w+\b')
sparse_matrix = cv.fit_transform(documents)
dense_matrix = sparse_matrix.todense()
td_matrix = dense_matrix.T
sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_

def rewrite_token(t):
    d = {"and": "&", "AND": "&",
     "or": "|", "OR": "|",
     "not": "1 -", "NOT": "1 -",
     "(": "(", ")": ")"}
    return d.get(t, 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t)) # Make retrieved rows dense

def rewrite_query(query): # rewrite every token in the query
    return " ".join(rewrite_token(t) for t in query.split())

# This function is just for testing and interferes when printing:
# def test_query(query):
#     print("Query: '" + query + "'")
#     print("Rewritten:", rewrite_query(query))
#     print("Matching:", eval(rewrite_query(query))) # Eval runs the string as a Python command
#     print()

def print_results():
    hits_matrix = eval(rewrite_query(user_input)) #!
    hits_list = list(hits_matrix.nonzero()[1])
    for i, doc_idx in enumerate(hits_list):
        print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))

user_input = "0"
while user_input != "":
    user_input = input("Write the query (press enter to stop): ").lower()
    try:
        if user_input == "":
            break
        else:
            print_results()
    except KeyError:
        print("Bad query")
