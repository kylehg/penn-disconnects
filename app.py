"""
Create the application.
"""
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        try:
            data = {
                'name': request.form['name'],
                'email': request.form['email'],
                'is_insterested': request.form['is_interested'],
                }
        except KeyError:
            return jsonify(error='Invalid form submission',
                           data=request.form)
        else:
            return jsonify(data=data)
    else:
        return 'Hello world!'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
