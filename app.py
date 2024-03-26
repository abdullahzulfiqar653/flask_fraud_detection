from flask import Flask, render_template, request, redirect, url_for, flash,session
import pandas as pd
import os
from utils import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signin')
def login():
    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_route():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_created = signup(username, email, password)
        if not is_created:
            return render_template('signup.html', error="username or email already exist")
        return redirect(url_for('login_route'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = get_users()
        for user in users:
            if username == user[0] and password == user[2]:  
                session['username'] = username
                return redirect(url_for('upload_file'))
        return render_template('signin.html', error="Invalid username or password.")
    return render_template('signin.html')



@app.route('/dashboard', methods=['POST', 'GET'])
def upload_file():
    transactions = []
    if 'username' in session:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if not file:
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File successfully uploaded')
                # Process the uploaded file
                if filename.endswith('.csv'):
                    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                elif filename.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                else:
                    flash('Unsupported file format')
                    return redirect(request.url)
                
                transactions = prepare_data_for_template(df)
                # fraud_transactions = check_fraud_transactions(transactions)

                return render_template('dashboard.html',cards_data=count_fraud_valid_transactions(df), transactions=transactions, username=session['username'])
            else:
                flash('Invalid file format')
                return redirect(request.url)
        return render_template('dashboard.html', cards_data=count_fraud_valid_transactions(), transactions=transactions, username=session['username'])
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
