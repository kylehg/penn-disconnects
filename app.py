"""
Create the application.
"""
import os
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            inter = 
#            print inter
            data = {
                'name': request.form['name'],
                'email': request.form['email'],
                'is_insterested': request.form.get('is_interested', False, type=bool)
                }
        except KeyError:
            return jsonify(error='Invalid form submission',
                           data=request.form)
        else:
            print data
            return jsonify(data=data)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
