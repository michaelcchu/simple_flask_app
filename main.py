import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, render_template
import json
import money

app = Flask(__name__)

@app.route('/mpc_m', methods=['GET','POST'])
def mpc_m():
    condensedMoney = []
    condensedProbs = []
    filename = ''
    deck = {}
    displayImage = False

    if request.method == 'POST':
        deck = json.loads(request.form['deck'].replace("'","\""))
        [condensedMoney,condensedProbs,filename] = money.main(deck,app)
        displayImage = True
    return render_template('mpc_m.html', filename=filename, deck=deck, money=condensedMoney, probs=condensedProbs, displayImage=displayImage)

@app.route('/mpc_s')
def mpc_s():
    return render_template('mpc_s.html')

@app.route('/hpc_m')
def hpc_m():
    return render_template('hpc_m.html')

@app.route('/sc_s')
def sc_s():
    return render_template('sc_s.html')

@app.route('/')
def home():
    return render_template('home.html')