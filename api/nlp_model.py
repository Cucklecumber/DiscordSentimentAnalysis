from unittest.util import _MAX_LENGTH
import tensorflow as tf
import numpy as np
import pickle
from keras.callbacks import ModelCheckpoint
from torch import embedding
import os
from keras.models import load_model

train = False
model_file = 'best_rnn_model.hdf5'

with open('preppedData.pkl', 'rb') as f:
    vocab_size, embedding_dim, max_length, train_labels, test_labels, train_reviews, test_reviews, tokenizer = pickle.load(f)
    

if train:
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_length), #each word is represented by 16 dimensional vector
        tf.keras.layers.LSTM(15, dropout=0.5),
        #tf.keras.layers.GlobalAveragePooling1D(),
        tf.keras.layers.Dense(15, activation='relu'),
        tf.keras.layers.Dense(6, activation='relu'),
        tf.keras.layers.Dense(3, activation='softmax') #better for probablity outputs
    ])

    model_file = 'best_lstm_model.h5'
    checkpoint = ModelCheckpoint(model_file, monitor='val_accuracy', verbose=1, save_best_only=True, mode='auto', preiod=1, save_weights_only=False)

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.summary()

    training_labels = np.array(train_labels)
    testing_labels = np.array(test_labels)

    num_epochs = 100
    history = model.fit(train_reviews, training_labels, epochs=num_epochs, validation_data=(test_reviews, testing_labels), callbacks=[checkpoint])
    
