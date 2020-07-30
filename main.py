import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, render_template
import json
import money

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    displayImage = False
    condensedMoney = []
    condensedProbs = []
    filename = ''
    deck = {}

    if request.method == 'POST':
        deck = json.loads(request.form['deck'].replace("'","\""))
        [condensedMoney,condensedProbs,filename] = money.main(deck,app)
        displayImage = True
    return render_template('index.html', filename=filename, deck=deck, money=condensedMoney, probs=condensedProbs, displayImage=displayImage)