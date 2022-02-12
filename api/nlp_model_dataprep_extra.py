import re

import nltk
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer


def pos_tagger(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:         
        return None
 
    
def prep_reviews(review):
    
    # remove all special characters
    processed_review = re.sub(r'\W', ' ', str(review))
    
    # remove all single characters
    processed_review = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_review)
 
    # Remove single characters from the start
    processed_review = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_review) 
 
    # Substituting multiple spaces with single space
    processed_review= re.sub(r'\s+', ' ', processed_review, flags=re.I)
 
    # Removing prefixed 'b'
    processed_review = re.sub(r'^b\s+', '', processed_review)
 
    # Converting to Lowercase
    processed_review = processed_review.lower().split(' ')
    
    stopwordsList = stopwords.words('english')
    processed_review = [w for w in processed_review if not w in stopwordsList] #Get rid of stop words
    
    pos_tagged = nltk.pos_tag(processed_review) #word tokenize splits list into seperate words, not need because earlier step, gets Part of Speech
    
    
    lemmatizer = WordNetLemmatizer()
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged)) #returns tuple of original word, and Part of speech
    
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            lemmatized_sentence.append(word)
        else:
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    
    return lemmatized_sentence