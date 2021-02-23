from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import io
import numpy as np
import nltk
from nltk.stem import PorterStemmer
import copy
stemmer = PorterStemmer() # made it global


def stemming(list):
    for i in range(len(list)):
        words = nltk.word_tokenize(list[i]) 
        words = [stemmer.stem(word) for word in words]                        
        list[i] = ' '.join(words)

    return list


def title_list():
    """ Read a file and make a list with titles of the document """
    title_list = []

    f = io.open("data100.txt", mode="r", encoding="utf-8" )
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


def terms_exists(query):
    return all(word in terms for word in query)     # returns True if every word in the query exists in our terms


def print_results(user_input):
    user_input_string = ' '.join([str(elem) for elem in user_input]) 

    try:
        if terms_exists(user_input):
            query_vec5 = tfv5.transform([user_input_string]).tocsc()
            hits = np.dot(query_vec5, sparse_matrix)
            ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
            for score, i in ranked_scores_and_doc_ids:
                first_occurrence = -1   
                while first_occurrence == -1:  
                    for word in user_input:
                        first_occurrence = stemmed_documents[i].find(word)     
                print("The score of {} is {:.4f} in document: {:s}".format(user_input_string, score, documents[i][:50]))           #[first_occurrence:first_occurrence+50]))
        else:
            print("No matching documents for query \"{}\"".format(user_input_string))
    except:
        print("Bad query")

documents = prepare_data()
documents_copy = copy.deepcopy(documents)
stemmed_documents = stemming(documents_copy) 
tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r'(?u)\b\w+\b')
sparse_matrix = tfv5.fit_transform(stemmed_documents).T.tocsr() # CSR: compressed sparse row format => order by terms
terms = tfv5.get_feature_names() # dictionary of terms


def main():
    user_input = "0"
    while user_input != "":
        user_input = input("Write the query (press enter to stop): ").lower()
        try:
            if user_input == "":
                break
            else:
                user_input = stemming(user_input.split())
                print_results(user_input)
        except KeyError:
            print("Bad query")
main()


