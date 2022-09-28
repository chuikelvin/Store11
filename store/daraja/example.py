import base64
from datetime import datetime

import requests
from requests.auth import HTTPBasicAuth


import keys

def formatted_time():
    unformatted = datetime.now()
    formatted =unformatted.strftime("%Y%m%d%H%M%S")
    return formatted

current_time = formatted_time()
data_to_encode =keys.business_ShortCode + keys.lipa_na_mpesa_passkey + current_time
encoded_string =base64.b64encode(data_to_encode.encode())
decoded_binary =encoded_string.decode('utf-8')

# print(decoded_binary)

consumer_key = keys.consumer_key
consumer_secret = keys.consumer_secret
api_URL = ("https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials")

data_to_encode =keys.consumer_key + keys.consumer_secret
encoded_string =base64.b64encode(data_to_encode.encode())
basic_authorization =encoded_string.decode('utf-8')

print(basic_authorization)

response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': "Bearer %s" % basic_authorization })
print(response.text.encode('utf8'))

# response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Bearer N0VEUU5wMXRObFE0R2NHeENYQlFyRWRpNXdaZWpPRXM6aUhROTJBa1lic1BoWVdFRw==' })
# print(response.text.encode('utf8'))

# headers = {"Authorization": "Bearer %s" % basic_authorization}

# r = requests.get(api_URL, auth =HTTPBasicAuth(consumer_key, consumer_secret))
# r = requests.get(api_URL, headers=headers)
# json_response = r.json()

# my_access_token = json_response['access_token']
# my_access_token = "Fm7L9LKaCYxULyZxrdbIz9tkSCeS"
# print(my_access_token)




def lipa_na_mpesa():
    access_token = my_access_token
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token,
    'Content-Type': 'application/json',}
    request = {
        "BusinessShortCode": keys.business_ShortCode,
        "Password": decoded_binary,
        "Timestamp": current_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": keys.phone_number,
        "PartyB": keys.business_ShortCode,
        "PhoneNumber": keys.phone_number,
        "CallBackURL": "https://mydomain.com/pat",
        "AccountReference": "Test",
        "TransactionDesc": "Test"
    }
    print(headers["Authorization"])
    # print(request["Timestamp"])
    # response = requests.post(url, json=request, headers=headers)
    # print(response.text)

# lipa_na_mpesa()
# print(time)
# print(request["Timestamp"])
# response = requests.post(url, json=request, headers=headers)

# print(response.text)

# Consumer Key: 7EDQNp1tNlQ4GcGxCXBQrEdi5wZejOEs
# Consumer Secret: iHQ92AkYbsPhYWEG
