import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, render_template
import json
import mpc_mScript
import hpc_mScript
import sc_sScript

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
        [condensedMoney,condensedProbs,filename] = mpc_mScript.main(deck,app)
        displayImage = True
    return render_template('mpc_m.html', filename=filename, deck=deck, money=condensedMoney, probs=condensedProbs, displayImage=displayImage)

@app.route('/mpc_s')
def mpc_s():
    return render_template('mpc_s.html')

@app.route('/hpc_m', methods=['GET','POST'])
def hpc_m():
    hands = []
    probs = []
    deck = {}
    display = False

    if request.method == 'POST':
        deck = json.loads(request.form['deck'].replace("'","\""))
        [hands,probs] = hpc_mScript.main(deck,app)
        display = True
    return render_template('hpc_m.html', deck=deck, hands=hands, probs=probs, display=display)

@app.route('/sc_s', methods=['GET','POST'])
def sc_s():
    text = ""
    display = False
    if request.method == 'POST':
        simChoice = request.form['simChoice']
        text = sc_sScript.main(simChoice)
        display = True
    return render_template('sc_s.html', text=text, display=display, request=request)

@app.route('/')
def home():
    return render_template('home.html')