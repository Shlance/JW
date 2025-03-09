import pymongo
from flask import Flask, render_template, request, redirect, flash
from bson.objectid import ObjectId
from random import sample, shuffle

app = Flask('jumbledwords')
app.config['SECRET_KEY'] = 'safe^&*hdgahksdg'

client = pymongo.MongoClient('mongodb+srv://YW:youngwonks@cluster0.odbmgfe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.jumbledwords


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        if 'addWord' in request.form and request.form['addWord']:
            document = {}
            document['word'] = request.form['addWord']
            db.words.insert_one(document)
            flash('Successfully added word.')
            return redirect('/')


@app.route('/play', methods=['GET', 'POST'])
def play():
    if request.method == 'GET':
        words = db.words.find()
        jumbled_words = []
        for word in words:
            jumbled_word = list(word['word'])
            shuffle(jumbled_word)
            jumbled_words.append({'_id': word['_id'], 'word': ''.join(jumbled_word)})
        jumbled_words = sample(jumbled_words, len(jumbled_words))
        return render_template('play_game.html', jumbledwords=jumbled_words)
    if request.method == 'POST':
        score = 0
        correctanswers = []
        useranswer = []
        print(request.form)  #immutable dict
        for word in list(request.form)[:-1]:
            #word here is the key as request.form is a dictionary
            correctanswers.append(db.words.find_one({'_id': ObjectId(word)})['word'].upper())
            useranswer.append(request.form[word].upper())
            if useranswer[-1] == correctanswers[-1]:
                score += 1

        return render_template('result.html', score=score, user_answer=useranswer, correct_answer=correctanswers,size= len(list(request.form))-1)



app.run(debug=True)