import requests

message = '106長者處於危險區域請留意長者狀況'
url = 'https://notify-api.line.me/api/notify'
TOKEN = 'ZkUeigqaMEkxKBi5oRRwC8Lo7DyBzZj3PZMDZDdLH5y'  # Ensure this is your correct token
headers = {
    'Authorization': 'Bearer ' + TOKEN
}
data = {
    'message': message
}

response = requests.post(url, headers=headers, data=data)
print(response.text)
