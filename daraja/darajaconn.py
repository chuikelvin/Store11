import requests
import os
import sys
from requests.auth import HTTPBasicAuth
import json

from access_token import generate_access_token
from encode import generate_password
from utils import get_timestamp
import keys

# BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append('daraja')


def lipa_na_mpesa(phone_number,ammount,order_details,domain):
    formatted_time = get_timestamp()
    decoded_password = generate_password(formatted_time)
    access_token,state = generate_access_token()
    if state == False:
        return 'no val',False
        print('unsuccessful')
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {"Authorization": "Bearer %s" % access_token}

    request = {
        "BusinessShortCode": keys.business_shortCode,
        "Password": decoded_password,
        "Timestamp": formatted_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": ammount,
        "PartyA": phone_number,
        "PartyB": keys.business_shortCode,
        "PhoneNumber": phone_number,
        "CallBackURL": domain,
        "AccountReference": order_details,
        "TransactionDesc": "Pay School Fees",
    }

    response = requests.post(api_url, json=request, headers=headers)
    responsedict=json.loads(response.text)
    # print(response)
    # print(responsedict)
    # print(responsedict['MerchantRequestID'])
    # print(responsedict['CheckoutRequestID'])
    return responsedict['CheckoutRequestID'],True

    # print(response.text)