from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, SelectField
import functions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

secret_word = None
word_set = None
to_display = None
tries = None
blanks = None
score_win = None
score_lose = None

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
	
    def __init__(self, username, password, email, victory) -> None:
        self.username = username
        self.password = password
        self.email = email


class WinLoss(db.Model, User):
	win_score = db.Column("Games won", db.Float, nullable=False)
	lose_score = db.Column("Games loss", db.Float, nullable=False)

# @app.after_request
# def set_response_headers(response):
#     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#     response.headers['Pragma'] = 'no-cache'
#     response.headers['Expires'] = '0'
#     return response

@app.route('/', methods=['GET'])
def index():
    if session.get('logged_in'):
        return render_template('home.html')
    else:
        return render_template('index.html', message="Hello!")


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            db.session.add(User(username=request.form['username'], password=request.form['password'], email=request.form['email']))
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(username=u, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('index.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))

@app.route('/game')
def game():
	global secret_word 
	global word_set
	global to_display
	global tries
	global blanks	
	secret_word = functions.get_random_word()
	word_set = "abcdefghijklmnopqrstuvwxyz"
	blanks = 0
	to_display = []
	for i,char in enumerate(secret_word):
		if char==" ":
			to_display.append(" ")
			
		else:
			to_display.append("_")
			blanks+=1

	tries = 0
	return render_template('game.html',to_display=to_display,word_set=word_set,tries="/static/img/hangman%d.png"%tries)


@app.route('/add_char',methods=["POST"])
def add_char():
	global secret_word
	global word_set
	global to_display
	global tries
	global blanks

	letter = request.form["letter"]
	
	chance_lost = True
	for i,char in enumerate(secret_word):
		if char==letter:
			chance_lost = False
			to_display[i] = letter
			blanks-=1

	word_set = word_set.replace(letter,'')
	print("blanks",blanks)
	if chance_lost==True:
		tries += 1
		if tries==10:
			return redirect('/game_lost')


	if blanks==0:
		return redirect('/game_won')

	return render_template('game.html',to_display=to_display,word_set=word_set,tries="/static/img/hangman%d.png"%tries)


@app.route('/game_lost')
def game_lost_landing():
	return render_template('game_lost.html')

@app.route('/game_won')
def game_won_landing():
	return render_template('game_won.html')


if(__name__ == '__main__'):
    app.secret_key = "ThisIsNotASecret:p"
    db.create_all()
    app.run()

