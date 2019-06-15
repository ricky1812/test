from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Event(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	event_name=db.Column(db.Text, unique=True, nullable=False)
	event_description=db.Column(db.Text, nullable=False)
	date_time=db.Column(db.DateTime, nullable=False)
	mails=db.relationship('Mail',backref='author',lazy=True)
	
	def __repr__(self):
		return f"User('{self.id},{self.event_name},{self.date_time}')"

class Mail(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	mail_id=db.Column(db.Text, unique=True)
	user_id=db.Column(db.Integer, db.ForeignKey('event.id'))

	def __repr__(self):
		return f"User('{self.user_id},{self.mail_id}')"

db.drop_all()
db.create_all()


@app.route('/', methods=["GET","POST"])
def home():
	if request.form:
		print(request.form)
		date_string=request.form.get("datetime")
		date_object = datetime.strptime(date_string, "%m/%d/%Y %H:%M %p")
		td=Event(event_name=request.form.get('event'), date_time=date_object, event_description=request.form.get('event_description'))
		db.session.add(td)
		db.session.commit()

	events=Event.query.all()
	return render_template('homepage.html',events=events)

@app.route('/gmail', methods=["GET","POST"])
def gmail():
	if request.form:
		print(request.form)
		user=Event.query.first()
		gd=Mail(mail_id=request.form.get('email_id'),user_id=user.id)
		db.session.add(gd)
		db.session.commit()
	emails=Mail.query.all()
	events=Event.query.all()
	return render_template('gmail.html',emails=emails,events=events)




if __name__=="__main__":
	debug=True




