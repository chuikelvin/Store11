import requests
import os
import sys
from requests.auth import HTTPBasicAuth

from access_token import generate_access_token
from encode import generate_password
from utils import get_timestamp
import keys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('daraja')


def lipa_na_mpesa():
    formatted_time = get_timestamp()
    decoded_password = generate_password(formatted_time)
    access_token = generate_access_token()

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {"Authorization": "Bearer %s" % access_token}

    request = {
        "BusinessShortCode": keys.business_shortCode,
        "Password": decoded_password,
        "Timestamp": formatted_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "3",
        "PartyA": keys.phone_number,
        "PartyB": keys.business_shortCode,
        "PhoneNumber": keys.phone_number,
        "CallBackURL": "https://mydomain.com/pat",
        "AccountReference": "test aware",
        "TransactionDesc": "Pay School Fees",
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


# lipa_na_mpesa()