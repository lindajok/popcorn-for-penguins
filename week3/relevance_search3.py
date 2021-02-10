from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import io
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.corpus import stopwords                         # in case we want to use stop words
stemmer = PorterStemmer() # made it global

def stemming(documents):
    for i in range(len(documents)):
        # toknize all the words in the documents
        words = nltk.word_tokenize(documents[i])           
        # stem all the words                                # if we want to use stop words, add code below:
        words = [stemmer.stem(word) for word in words]      # if word not in set(stopwords.words('english'))]   
        # join the stemmed word into sentences                      
        documents[i] = ' '.join(words)

    return documents


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


# The original output from the tutorial:
def print_results(user_input):
    documents = stemming(prepare_data())
    tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    sparse_matrix = tfv5.fit_transform(documents).T.tocsr() # CSR: compressed sparse row format => order by terms
    query_vec5 = tfv5.transform([user_input]).tocsc()
    hits = np.dot(query_vec5, sparse_matrix)

    ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
    for score, i in ranked_scores_and_doc_ids:
        first_occurrence = documents[i].find(user_input)
        print("The score of {} is {:.4f} in document: {:s}".format(user_input, score, documents[i][first_occurrence:first_occurrence+50]))


######################################################################
## Commented this for now because it doesn't work correctly and     ##
## makes it hard to evaluate if the actual code works properly -->  ##
######################################################################
# def print_results(user_input):
#     titles = title_list() # A list of title names
#     documents = prepare_data() # Documents in a list of strings format

#     tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
#     sparse_matrix = tfv5.fit_transform(documents).T.tocsr() # CSR: compressed sparse row format => order by terms
#     query_vec5 = tfv5.transform([user_input]).tocsc()
#     hits = np.dot(query_vec5, sparse_matrix)
#     ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

#     for score, i in ranked_scores_and_doc_ids:
#         cut = documents[i]
#         first_occurrence = cut.find(user_input)

#         if first_occurrence == -1:
#             print("The input not found")
#         else:
#             print("The score of {} is {:.4f} in document {}: {:s}{:s}...".format(user_input, score,
#                 titles[i], cut[first_occurrence-50:first_occurrence], cut[first_occurrence:first_occurrence+50]))


# ---------------------- New code here too -------------------------

#tokenize(prepare_data()) # calling the function tokenize
stemming(prepare_data()) # calling the function stemming --> stemming(tokenize(prepare_data)))
# --> I really don't know what to do with them next ((⇀‸↼))
# You can try to print these two functions with a smaller dataset so
# you know how the output looks like. Also this implementation is
# a bit slow.

# -------------------------------------------------------------------


def main():
    user_input = "0"
    while user_input != "":
        user_input = input("Write the query (press enter to stop): ").lower()
        user_input = nltk.word_tokenize(user_input)
        user_input = [stemmer.stem(word) for word in user_input]
        user_input = ' '.join([word for word in user_input])
        try:
            if user_input == "":
                break
            else:
                print_results(user_input)
        except KeyError:
            print("Bad query")
main()


