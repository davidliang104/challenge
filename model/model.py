import os
# Hide tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.models import load_model
import pickle
import numpy as np
import string
import re
from keras.preprocessing.text import Tokenizer
from keras.utils.data_utils import pad_sequences

class Translator:
    def __init__(self):
        self.model = load_model("model/model.h5")
        print("model loaded")
    
    def process(self, sentence):
        # Load English tokenizer
        eng_tokenizer = Tokenizer()
        with open('model/eng_tokenizer.pickle', 'rb') as handle:
            eng_tokenizer = pickle.load(handle)
        
        # Convert to lowercase and remove punctuation
        sentence = sentence.lower()
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        sentence = re.sub(' {2,}', ' ', sentence)

        # Convert sentence into array
        sentence_arr = np.array([sentence])
        # Tokenize and pad sentence
        tokens = eng_tokenizer.texts_to_sequences(sentence_arr)
        padded = pad_sequences(tokens, maxlen=15, padding='post')

        print("sentence cleaned")

        return padded

    def predict(self, sentence):
        sentence = self.process(sentence)

        # Compute prediction vector
        pred_vector = self.model.predict(sentence)
        print("predicted")
        # Load French tokenizer
        with open('model/fr_tokenizer.pickle', 'rb') as handle:
            fr_tokenizer = pickle.load(handle)
        
        # Get word with highest probability for each position and build translated sentence
        prediction = np.argmax(pred_vector, axis=2)
        result =  fr_tokenizer.sequences_to_texts(prediction)[0]
        print("translated")
        return result
