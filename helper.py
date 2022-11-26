import requests
import json




def check_tanadi_database(phone_number):
    print(phone_number)
    url = "https://api.tanadi.co/api/v1/ussd/user-info"

    payload = json.dumps({
    "phone_number": f"{phone_number}"
    })
    headers = {
    'Content-Type': 'application/json'
    }
    print(payload)
    response = requests.request("GET", url, headers=headers, data=payload)

    # print(response.text)
    # print(response.json().get("message"))
    return response.json().get("message")




# import requests
# import json

# url = "https://api.tanadi.co/api/v1/ussd/user-info"

# payload = json.dumps({
#   "phone_number": "+2347060900294"
# })
# headers = {
#   'Content-Type': 'application/json'
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
