"""
Create the application.
"""
import os
from urlparse import urlparse

from flask import Flask, jsonify, redirect, render_template, request, url_for
from pymongo import Connection

app = Flask(__name__)
MONGO_URL = os.environ.get('MONGOHQ_URL')
 
if MONGO_URL:
    connection = Connection(MONGO_URL) # Get a connection
    db = connection[urlparse(MONGO_URL).path[1:]] # Get the database
else:
    # Not on an app with the MongoHQ add-on, do some localhost action
    connection = Connection('localhost', 27017)
    db = connection['disconnects']


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
                'is_interested': request.form.get('is_interested', False, type=bool)
                }
            print 'Data: ', data
        except KeyError:
            return jsonify(error='Invalid form submission',
                           data=request.form)
        else:
            record = db.signups.find_one({'email': data['email']})
            if record is not None:
                print 'Old record: ', record
                db.signups.update({'email': record['email']}, {'$set': data})
            else:
                print 'Inserting new record'
                db.signups.insert(data)
            return jsonify(data=data)
    else:
        return redirect(url_for('home'))


@app.route('/dump')
def dump():
    signups = db.signups.find()
    return '<br/>'.join([','.join(str(v) for v in signup.values()) for signup in signups])


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
