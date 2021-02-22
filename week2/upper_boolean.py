from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import io
import re
import numpy as np
import enchant
import splitter


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


cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r'(?u)\b\w+\b', ngram_range=(1, 3)) # 1gram: ngram_range=(1,1), 2gram: ngram_range=(2,2), from 1gram to 3gram: ngram_range=(1, 3) ... etc
sparse_matrix = cv.fit_transform(documents)
dense_matrix = sparse_matrix.todense()
td_matrix = dense_matrix.T
sparse_td_matrix = sparse_matrix.T.tocsr()
t2i = cv.vocabulary_ # dictionary of terms
terms = cv.get_feature_names()
terms_textfile = enchant.request_pwl_dict("data100_wordlist_3gram.txt") # Defining a personal wordlist (= pwl)
unknownword_list = []

# TF-IDF
tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2", token_pattern=r'(?u)\b\w+\b')
sparse_matrix = tfv5.fit_transform(documents).T.tocsr()

# Make a file of list of words
f = open("data100_wordlist_3gram.txt", "w")
for k, v in t2i.items():
    f.write(k + "\n")
f.close()


def rewrite_token(t):
    d = {"AND": "&",
     "OR": "|",
     "NOT": "1 -",
     "(": "(", ")": ")"}

    # Hi guys... Here is some code for you. Made it extra spaghetti this time with hint of spice and double cheese, just get your brains working uknow? I'm just thinking about you and your wellbeing and not being very bad at coding. This comment is also very long, just so because I don't want you to read the code below. You can just continue reading this comment, or actually just skip it. Or skip the whole code while we are at it. Yes? Good? Okay you can now delete this comment, thanks.
    if t in d:
        return d.get(t)
    if t[0] == "\"" and t[-1] == "\"":
        t = t.replace("\"", "")
        try:
            t_ngram = ' '.join([str(t.lower()) for t in splitter.split(t)])
            if t_ngram in terms:
                return 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t_ngram)
            else:
                if t_ngram == "":
                    unknownword_list.append(t)
                else:
                    unknownword_list.append(t_ngram)
                return 'np.matrix(np.zeros(len(documents), dtype=int))'
        except:
            unknownword_list.append(t)
            return 'np.matrix(np.zeros(len(documents), dtype=int))'
    elif t.lower() in terms:
        return 'sparse_td_matrix[t2i["{:s}"]].todense()'.format(t.lower())
    else:
        if t[0] == "\"" or t[-1] == "\"":
            pass
        else:
            unknownword_list.append(t)
            return 'np.matrix(np.zeros(len(documents), dtype=int))'


def rewrite_query(query): 
    return " ".join(rewrite_token(t) for t in query.split())


def similar(w):
    """ Return similar word with most freq in docs (if found) """

    suggested_wordlist = terms_textfile.suggest(w)
    if suggested_wordlist:                                      # If there list is not empty:
        most_freq_score = 0.0
        most_freq_word = ""
        for suggestion in suggested_wordlist:
            query_vec5 = tfv5.transform([suggestion]).tocsc()   # CSC: compressed sparse column format 
            hits = np.dot(query_vec5, sparse_matrix)            # cosine similarity (dot product)
            ranked_scores = sorted(np.array(hits[hits.nonzero()])[0], reverse=True) # rank the documents by tf-idf scores (highest to lowest)
            highest_freq = ranked_scores[0]                     # choose the highest score (= the first one)
            if highest_freq > most_freq_score:                  
                most_freq_score = highest_freq                  
                most_freq_word = suggestion
        return most_freq_word
    else:
        return None


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
        print("Wrong syntax. Please check that you use uppercase boolean operators (AND, OR, NOT) and no spaces inside quotations.")

    global unknownword_list             # Global variable needs to be decleared
    if unknownword_list:                # If there is unkown words:
        for w in unknownword_list:
            similar_word = similar(w)   # Call for function "similar" to find a similar word
            if not similar_word:
                print("We didn't find anything matching \"{}\".".format(w))
            else:
                print("We didn't find anything matching \"{}\". Did you perhaps mean: {}?".format(w, similar_word))
    unknownword_list = []              


def main():
    print("Search for multi-word phrases INSIDE QUOTATIONS and WITHOUT spaces, e.g. \"newyork\".")
    print("Use UPPERCASED boolean operators, e.g. new AND york, new OR york, new NOT york")
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
