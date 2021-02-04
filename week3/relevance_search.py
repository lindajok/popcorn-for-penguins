documents = ["This is a silly silly silly example",
             "A better example",
             "Nothing to see here nor here nor here",
             "This is a great example and a long example too"]


# 

# # 
# # binary_dense_matrix = cv.fit_transform(documents).T.todense()

# dense_matrix = cv.fit_transform(documents).T.todense()

 

# # hits_list = np.array(dense_matrix[t2i["example"]])[0]


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

cv = CountVectorizer(lowercase=True, binary=True)
t2i = cv.vocabulary_ 
# tfv1 = TfidfVectorizer(lowercase=True, sublinear_tf=False, use_idf=False, norm=None)
# tf_matrix1 = tfv1.fit_transform(documents).T.todense()

# tfv2 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=False, norm=None)
# tf_matrix2 = tfv2.fit_transform(documents).T.todense()

tfv4 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
tf_matrix4 = tfv4.fit_transform(documents).T.todense()

hits_list4 = np.array(tf_matrix4[t2i["silly"]] + tf_matrix4[t2i["example"]])[0]
hits_and_doc_ids = [ (hits, i) for i, hits in enumerate(hits_list4) if hits > 0 ]
ranked_hits_and_doc_ids = sorted(hits_and_doc_ids, reverse=True)

query_vec4 = tfv4.transform(["silly example"]).todense() # creates a vector of our query

scores = np.dot(query_vec4, tf_matrix4)
ranked_scores_and_doc_ids = \
    sorted([ (score, i) for i, score in enumerate(np.array(scores)[0]) if score > 0], reverse=True)

for score, i in ranked_scores_and_doc_ids:
    print("The score of 'silly example' is {:.4f} in document: {:s}".format(score, documents[i]))


# -----

tfv5 = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
sparse_matrix = tfv5.fit_transform(documents).T.tocsr() # CSR: compressed sparse row format => order by terms

query_vec5 = tfv5.transform(["silly example"]).tocsc() # CSC: compressed sparse column format
hits = np.dot(query_vec5, sparse_matrix)

ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)
for score, i in ranked_scores_and_doc_ids:
    print("The score of 'silly example' is {:.4f} in document: {:s}".format(score, documents[i]))

# index --> 
gv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
g_matrix = gv.fit_transform(bookdata).T.tocsr()



