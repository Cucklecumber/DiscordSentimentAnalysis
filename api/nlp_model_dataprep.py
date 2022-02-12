from copyreg import pickle
from lib2to3.pgen2 import token
from multiprocessing import ProcessError
from matplotlib.pyplot import text, title

import pandas as pd
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

import pickle

import nltk
nltk.download('averaged_perceptron_tagger')
from nlp_model_dataprep_extra import prep_reviews, pos_tagger

df = pd.read_csv('amazon_baby.csv')
df = df.drop(['name'], 1)

def sort_ratings(score):
    if score in [1,2]:
        return 0 #negative
    elif score in [3]:
        return 1 #nuetral
    else:
        return 2 #positive
            

df['sentiments'] = df.rating.apply(sort_ratings)
df['filtered_review'] = df.review.apply(prep_reviews)

tokenizer = Tokenizer(oov_token="<OOV>")

split = round(len(df)*0.8)

train_reviews = df['filtered_review'][:split]
train_label = df['sentiments'][:split]
test_reviews = df['filtered_review'][split:]
test_label = df['sentiments'][split:]

vocab_size = 40000
embedding_dim = 16
max_length = 120
trunc_type = 'post'
oov_tok = '<OOV>'
padding_type = 'post'


tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_tok)
tokenizer.fit_on_texts(train_reviews)
word_index = tokenizer.word_index


sequences = tokenizer.texts_to_sequences(train_reviews)
training_padded_reviews = pad_sequences(sequences, maxlen=max_length, truncating=trunc_type)
testing_sentences = tokenizer.texts_to_sequences(test_reviews)
testing_padded_reviews = pad_sequences(testing_sentences, maxlen=max_length)


pkl_list_of_data = [vocab_size, embedding_dim, max_length, train_label, test_label, training_padded_reviews, testing_padded_reviews, tokenizer]


with open('preppedData.pkl', 'wb') as f:
    pickle.dump(pkl_list_of_data, f)
    