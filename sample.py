import re
import json
import streamlit as st

# List of target bank names
bank_names = ["OPAY", "SMART PAY", "UBA", "ECO BANK"]

# List of target keywords for airtime topup (excluding bank names)
airtime_keywords = ["airtime", "card", "topup", "recharge", "data", "bundle"]


def process_text(text):
    """
    Extracts numbers, identifies transaction types, separates transaction amounts and bank account numbers for money transfer,
    and handles airtime topup amounts and beneficiary numbers.
    """
    numbers = []  # List to store all extracted numbers
    bank_name = None
    transaction_type = None

    # Regular expression patterns
    number_pattern = r"\d+"  # Matches one or more digits
    bank_name_pattern = r"(?:\b" + r"\b|\s+".join(bank_names) + r"\b)"
    # Matches whole words from the list

    # Search for matches
    number_matches = re.findall(number_pattern, text)
    bank_name_match = re.search(bank_name_pattern, text, flags=re.IGNORECASE)  # Case-insensitive search

    # Extract values if found
    numbers = number_matches
    if bank_name_match:
        bank_name = bank_name_match.group()

    # Identify transaction type based on keywords and bank names (case-insensitive)
    if ("transfer" in text.lower() or "money" in text.lower()) and bank_name and len(numbers) >= 2:
        transaction_type = "money_transfer"
        numbers = number_matches[:2]  # Extract first two numbers for money transfer
    elif any(keyword in text.lower() for keyword in airtime_keywords) and len(number_matches) >= 2:
        transaction_type = "airtime_topup"
        # Extract only the first two numbers (assuming first is airtime amount, second is beneficiary number)
        numbers = number_matches[:2]

    return numbers, bank_name, transaction_type

# ... (rest of the code remains the same) ...

def add_to_database(numbers, bank_name, transaction_type):
    """
    Simulates adding information to separate databases based on transaction type.
    """
    if transaction_type == "money_transfer":
        if len(numbers) >= 2:
            amount, account_number = numbers
            data_file = "money_transfer.json"
            key = f"Transfer to {bank_name} - {account_number}"
        else:
            print("Insufficient numbers found for money transfer.")
            return  # Exit function if not enough numbers
    elif transaction_type == "airtime_topup":
        if len(numbers) >= 2:
            airtime_amount, beneficiary_number = numbers
            data_file = "airtime_topup.json"
            key = f"Topup to {beneficiary_number}"
        else:
            print("Insufficient numbers found for airtime topup.")
            return  # Exit function if not enough numbers

    # Add data to JSON file
    if transaction_type == "money_transfer":
        print(f"Your {transaction_type.title()} is being processed")
        with open(data_file, 'a+') as f:
            data = {
                "amount": airtime_amount if transaction_type == "airtime_topup" else amount,  # Use correct variable based on transaction type
                "bank_name": bank_name if transaction_type == "money_transfer" else None,  # Include bank_name for money transfer
                "account_number": account_number if transaction_type == "money_transfer" else beneficiary_number
            }
            json.dump(data, f, indent=4)
    elif transaction_type == "airtime_topup":
        print(f"Your {transaction_type.title()} is being processed")
        with open(data_file, 'a+') as f:
            data = {
                "amount": airtime_amount if transaction_type == "airtime_topup" else amount,  # Use correct variable based on transaction type
                "beneficiary_number": account_number if transaction_type == "money_transfer" else beneficiary_number
            }
            json.dump(data, f, indent=4)


def load_database(filename):
    """
    Loads data from a JSON file.
    """
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return empty list if file not found


def display_database(data):
    """
    Displays database content in a Streamlit table.
    """
    if data:
        st.header("Database Content")
        st.dataframe(data)
    else:
        st.info("No data found in the database.")


def main():
    # User input for text
    text = st.text_input("Enter your transaction details:")

