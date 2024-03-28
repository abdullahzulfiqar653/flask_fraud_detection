from flask import jsonify
import joblib
import numpy as np
from tensorflow import keras
from keras.layers import Dense
from flask import Flask, request, jsonify
from keras.models import Sequential, load_model

model = load_model('model.h5')
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}
vectorization_components = joblib.load('vectorize.pkl')
robust_scaler = vectorization_components['robust_scaler']
time_min = vectorization_components['time_min']
time_max = vectorization_components['time_max']


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
        for index, row in enumerate(data):
            transaction = {
                'id': index + 1,
                'time': row['Time'],
                'amount': row['Amount'],
                'class': row['Class'],
                'probability': round(row['fraud_probability'], 2)
            }
            transactions.append(transaction)
    return transactions

def signup(username, email, password):
    # Check if username or email already exists
    with open("users.txt", "r") as file:
        for line in file:
            existing_username, existing_email, _ = line.strip().split(",")
            if username == existing_username or email == existing_email:
                return False

    # If username and email do not exist, add the new entry
    with open("users.txt", "a") as file:
        file.write(f"{username},{email},{password}\n")
    return True

def get_users():
    with open("users.txt", "r") as file:
        return [line.strip().split(',') for line in file]

def get_json_data(df):
    transactions = []
    for index, row in df.iterrows():
        transaction = {
            "Time": row['Time'],
            "V1": row['V1'],
            "V2": row['V2'],
            "V3": row['V3'],
            "V4": row['V4'],
            "V5": row['V5'],
            "V6": row['V6'],
            "V7": row['V7'],
            "V8": row['V8'],
            "V9": row['V9'],
            "V10": row['V10'],
            "V11": row['V11'],
            "V12": row['V12'],
            "V13": row['V13'],
            "V14": row['V14'],
            "V15": row['V15'],
            "V16": row['V16'],
            "V17": row['V17'],
            "V18": row['V18'],
            "V19": row['V19'],
            "V20": row['V20'],
            "V21": row['V21'],
            "V22": row['V22'],
            "V23": row['V23'],
            "V24": row['V24'],
            "V25": row['V25'],
            "V26": row['V26'],
            "V27": row['V27'],
            "V28": row['V28'],
            "Amount": row['Amount'],
            "Class": str(row['Class'])  # Ensure Class is converted to string
        }
        transactions.append(transaction)
    return transactions

def make_assumptions(transactions):
    for data in transactions:
        features = [
                data['V1'], data['V2'], data['V3'], data['V4'], data['V5'],
                data['V6'], data['V7'], data['V8'], data['V9'], data['V10'],
                data['V11'], data['V12'], data['V13'], data['V14'], data['V15'],
                data['V16'], data['V17'], data['V18'], data['V19'], data['V20'],
                data['V21'], data['V22'], data['V23'], data['V24'], data['V25'],
                data['V26'], data['V27'], data['V28'],
            ]
        amount = data['Amount']
        time = data['Time']

        amount = float(amount)
        time = float(time)

        scaled_amount = robust_scaler.transform(np.array([[amount]]))
        scaled_time = (time - time_min) / (time_max - time_min)

        input_features = np.concatenate((features, scaled_amount.flatten(), [scaled_time]))

        prediction = model.predict(np.array([input_features]))
        data['fraud_probability'] = float(prediction[0][0])
        
    return prepare_data_for_template(transactions)
