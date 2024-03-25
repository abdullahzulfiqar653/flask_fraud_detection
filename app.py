from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
from werkzeug.utils import secure_filename

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

def count_fraud_valid_transactions(data = None):
    fraud_count = valid_count = 0
    if data is not None:
        fraud = data[data['Class'] == 1] 
        valid = data[data['Class'] == 0] 

        outlierFraction = len(fraud) / float(len(valid)) 
        fraud_count = len(fraud)
        valid_count = len(valid)
    return {
        'total': fraud_count+valid_count,
        'valid': valid_count,
        'fraud': fraud_count
    }

def prepare_data_for_template(data):
    # Function to prepare data with only four columns for rendering in the template
    # Assuming you need to add a transaction ID manually starting from 1
    transactions = []
    if data is not None:
        for index, row in data.iterrows():
            transaction = {
                'Transaction ID': index + 1,
                'Time': row['Time'],
                'Amount': row['Amount'],
                'Class': row['Class']
            }
            transactions.append(transaction)
    return transactions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin')
def login():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def upload_file():
    transactions = []
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

            return render_template('dashboard.html',cards_data=count_fraud_valid_transactions(df), transactions=transactions)
        else:
            flash('Invalid file format')
            return redirect(request.url)
    return render_template('dashboard.html', cards_data=count_fraud_valid_transactions(), transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
