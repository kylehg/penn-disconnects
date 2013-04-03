"""
Create the application.
"""
import os
import smtplib
from urlparse import urlparse

from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import Connection
from sendgrid import Message, Sendgrid

app = Flask(__name__)
NAME = 'Penn [Dis]Connects'
MONGO_URL = os.environ.get('MONGOHQ_URL')
SENDGRID_UN = os.environ.get('SENDGRID_USERNAME')
SENDGRID_PW = os.environ.get('SENDGRID_PASSWORD')
 
if MONGO_URL:
    connection = Connection(MONGO_URL) # Get a connection
    db = connection[urlparse(MONGO_URL).path[1:]] # Get the database
    DEBUG = False
    EMAIL = 'kylehardgrave+pdc@gmail.com'
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    connection = Connection('localhost', 27017)
    db = connection['disconnects']
    DEBUG = True
    EMAIL = 'penndisconnects@gmail.com'

BYLINE = (EMAIL, NAME)

if not (SENDGRID_UN and SENDGRID_PW):
    from config import SENDGRID_UN, SENDGRID_PW
sg = Sendgrid(SENDGRID_UN, SENDGRID_PW)



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            data = {
                'name': request.form['name'],
                'email': request.form['email'],
                'is_interested': request.form.get('is_interested', False,
                                                  type=bool)
                }
            print 'Data: ', data
        except KeyError:
            return jsonify(error='Invalid form submission',
                           data=request.form)

        record = db.signups.find_one({'email': data['email']})
        if record is not None:
            print 'Old record: ', record
            db.signups.update({'email': data['email']}, {'$set': data})
        else:
            print 'Inserting new record'
            db.signups.insert(data)
        print 'Data2: ', data
        send_emails(data)
        data = {
            'name': data['name'],
            'email': data['email'],
            'is_interested': data['is_interested']
            }
        return jsonify(data=data)
    else:
        return redirect(url_for('home'))


def send_emails(data):
    """Send sign-up e-mails."""
    if data['is_interested']:
        us_subj = 'New Leader'
        us_body = render_template('leader-us.html', **data)
    else:
        us_subj = 'New Pledge'
        us_body = render_template('pledge-us.html', **data)
        them_subj = 'Congrats on pledging to disconnect!'
        them_body = render_template('pledge-them.html', **data)

        them_msg = Message(BYLINE, them_subj, them_body, them_body)
        them_msg.add_to(data['email'], data['name'])
        sg.smtp.send(them_msg)

    us_msg = Message(BYLINE, '[PDC] %s' % us_subj, us_body, us_body)
    us_msg.add_to(EMAIL, NAME)
    us_msg.set_replyto(data['email']) # Reply-to them by default
    sg.smtp.send(us_msg)


def dump_signups(signups):
    return 'Count: %s<br/>%s' % (
        signups.count(),
        '<br/>'.join([','.join(str(v) for v in signup.values())
                      for signup in signups]))


@app.route('/dump')
def dump():
    """See all the signups."""
    return dump_signups(db.signups.find())


@app.route('/leaders')
def leaders():
    """See all the leaders."""
    return dump_signups(db.signups.find({'is_interested': True}))
    


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)
