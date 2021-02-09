from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import io
import numpy as np


def title_list():
    """ Read a file and make a list with titles of the document """
    title_list = []
    f = io.open("gutenberg.txt", mode="r", encoding="utf-8" )
    for line in f:
        line = line.replace('\n', '')
        if "<article name=" in line:
            line = line.replace('<article name="', '')
            line = line.replace('">', '')
            title_list.append(line)
    f.close()

    return title_list


def prepare_data():
    """ Read a file and make a list of strings """
    documents = []
    article = ""
    f = io.open("gutenberg.txt", mode="r", encoding="utf-8" )    
    
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


def print_results(user_input):
    titles = title_list() # A string of title names
    documents = prepare_data() # Documents in a list of strings format

    tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    sparse_matrix = tfv5.fit_transform(documents).T.tocsr() # CSR: compressed sparse row format => order by terms

    query_vec5 = tfv5.transform([user_input]).tocsc()
    hits = np.dot(query_vec5, sparse_matrix)

    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
    for score, i in ranked_scores_and_doc_ids:
        print("The score of {} is {:.4f} in document: {:s}...".format(user_input, score, documents[i][:50]))


def main():
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
main()


