ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}

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