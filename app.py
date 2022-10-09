import os
from flask import Flask, render_template, request
from model.model import Translator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/translate", methods=['GET', 'POST'])
def translate():
    # Get sentence from form
    sentence = request.form["sentence"]
    print("got sentence")
    # Create instance
    model = Translator()
    print("got translator")
    # Get prediction
    result = model.predict(sentence)

    return render_template('index.html', res = result)
  
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)