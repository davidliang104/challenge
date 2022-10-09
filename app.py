import os
# Hide tensorflow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import pickle
import numpy as np
import string
import re
from keras.preprocessing.text import Tokenizer
from keras.utils.data_utils import pad_sequences

app = Flask(__name__)

# # Load model
model = load_model("model/model.h5")

@app.route('/')
def fun():
    return render_template('index.html')

@app.route("/", methods=['GET', 'POST'])
def predict():
    # Get sentence from form
    sentence = request.form["sentence"]

    # Load English and French tokenizers
    eng_tokenizer = Tokenizer()
    fr_tokenizer = Tokenizer()
    with open('model/eng_tokenizer.pickle', 'rb') as handle:
        eng_tokenizer = pickle.load(handle)
    with open('model/fr_tokenizer.pickle', 'rb') as handle:
        fr_tokenizer = pickle.load(handle)

    # Convert to lowercase and remove punctuation
    sentence = sentence.lower()
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    sentence = re.sub(' {2,}', ' ', sentence)

    # Convert sentence into array
    sentence_arr = np.array([sentence])
    # Tokenize and pad sentence
    tokens = eng_tokenizer.texts_to_sequences(sentence_arr)
    padded = pad_sequences(tokens, maxlen=15, padding='post')
    # Compute prediction vector
    pred_vector = model.predict(padded)
    # Get word with highest probability for each position and build translated sentence
    prediction = np.argmax(pred_vector, axis=2)
    result =  fr_tokenizer.sequences_to_texts(prediction)[0]
    return render_template('index.html', res = result)
  
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)