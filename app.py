from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
approved = 10
rejected = 5
pending_review = 3
cards_data = {
    'approved': approved,
    'rejected': rejected,
    'pending_review': pending_review
}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_fraud_transactions(transactions):
    # Here you can implement your logic to check for fraud transactions
    # For demonstration purposes, let's assume fraud transactions are transactions with amount > 1000
    fraud_transactions = [t for t in transactions if t['Amount'] > 1000]
    return fraud_transactions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def login():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Simulated data for demonstration
    
    transactions = []
    fraud_transactions = []
    return render_template('dashboard.html', cards_data=cards_data, transactions=transactions, fraud_transactions=fraud_transactions)

@app.route('/upload', methods=['POST'])
def upload_file():
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
        
        transactions = df.to_dict('records')
        fraud_transactions = check_fraud_transactions(transactions)

        return render_template('dashboard.html',cards_data=cards_data, transactions=transactions, fraud_transactions=fraud_transactions)
    else:
        flash('Invalid file format')
        return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)