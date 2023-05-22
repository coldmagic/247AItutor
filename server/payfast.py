#Server/payfast.py:
#This is a module that provides the PayFast service for the app. 
#It imports requests library and creates a PayFast class that handles the payment processing using the PayFast API. 
#It also defines methods for creating a payment request, verifying a payment notification and canceling a payment subscription.



import hashlib
import urllib.parse
import requests
import socket
from werkzeug.urls import url_parse

# generates a PayFast security signature.
def generate_signature(data: dict, passphrase: str = '') -> str:
    data_items = sorted(data.items())
    data_str = '&'.join(f"{k}={urllib.parse.quote_plus(str(v))}" for k, v in data_items if v)
    if passphrase:
        data_str += f"&passphrase={passphrase}"

    return hashlib.md5(data_str.encode()).hexdigest()

# verifies the signature sent by PayFast in the ITN.
def pfValidSignature(data: dict, passphrase: str = '') -> bool:
    signature = data.pop('signature', None)
    new_signature = generate_signature(data, passphrase)
    return signature == new_signature

# This function checks if the ITN has come from a valid PayFast domain.
def pfValidIP() -> bool:
    valid_hosts = [
        'www.payfast.co.za',
        'sandbox.payfast.co.za',
        'w1w.payfast.co.za',
        'w2w.payfast.co.za',
    ]
    host = url_parse(request.url).host
    return host in valid_hosts

# compares the `amount_gross` value sent in the ITN with the expected amount.
def pfValidPaymentData(expected_amount: float, data: dict) -> bool:
    amount_gross = float(data.get('amount_gross', '0.0'))
    return abs(amount_gross - expected_amount) <= 0.01

# sends a request back to the PayFast server to confirm the details of the transaction.
def pfValidServerConfirmation(data: dict, passphrase: str = '', pfHost = 'sandbox.payfast.co.za') -> bool:
    url = f"https://{pfHost}/eng/query/validate"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    pfParamString = generate_signature(data, passphrase)
    response = requests.post(url, data=pfParamString, headers=headers)
    return response.text == 'VALID'
