import os
from sqlite3 import Timestamp
from keras.models import load_model
from pandas import period_range
from nlp_model_dataprep_extra import prep_reviews, pos_tagger
import pickle
from keras.preprocessing.sequence import pad_sequences
from discord_scraper import scrape_messages

token = 'NzE3NTM5Mjk3NDg5NzE1MjUx.YGuq5g.pk6177YgMggmoJE1j5s6S6E8Vl8'
channel_id = '941499119145484321'

model_file = 'best_lstm_model.hdf5'

with open('preppedData.pkl', 'rb') as f:
    vocab_size, embedding_dim, max_length, unneeded0, unneeded1, unneeded2, unneeded3, tokenizer = pickle.load(f)
    
if os.path.isfile(model_file):      
    model = load_model(model_file)

def weight_prediction_output(output):
    prediction = output[0]
    
    if prediction[2] > 0.2:

        weighted_prediction = [prediction[0] + 0.15, prediction[1] + 0.1, prediction[2] - 0.25]
        weighted_prediction = [round(i, 2) for i in weighted_prediction]
    
    return weighted_prediction
    
def classify_text(text):
    sequences = tokenizer.texts_to_sequences([text])
    text = pad_sequences(sequences, maxlen=max_length, truncating='post')
    #print(tokenizer.sequences_to_texts(text))
    prediction = model.predict(text)
    
    weighted_prediction = weight_prediction_output(prediction)
    return weighted_prediction

content, usernames, timestamps = scrape_messages(token, channel_id)

def assign_scores(score):
    list_sum = sum(score)
    if score[2] / list_sum > 0.8:
        print("IN LOVE")
        return(0)
    elif score[2] / list_sum > 0.4:
        if score[0] < 0.2:
            print("GOOD MATCH")
            return(1)
        elif score[0] > 0.2:
            print("NUETRAL")
            return(2)
    else:
        print("BAD MATCH")
        return(3)
        
    
total_predictions = [0, 0, 0]
user_prediction_scores = {}

for i in zip(content, usernames, timestamps):
    prediction = classify_text(content)
    total_predictions = [round(a + b, 2) for a, b in zip(total_predictions, prediction)]

    if i[1] not in user_prediction_scores: #create new user
        new_user = {str(i[1]): prediction}
        user_prediction_scores.update(new_user)
    else:
        old_prediction_score = user_prediction_scores[str(i[1])]
        updated_prediction_score = [round(a + b, 2) for a,b in zip(old_prediction_score, prediction)]
        edited_user = {str(i[1]): updated_prediction_score}
        user_prediction_scores.update(edited_user)

overall_judgement = assign_scores(total_predictions)
    
print(total_predictions)
print(user_prediction_scores)    
    