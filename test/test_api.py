import requests 
import json

# exec(open('../main.py').read())

base_url = 'http://localhost:8000/'

username = 'admin'
password = 'admin'

# 1. Login
response = requests.post(base_url + 'v1/login', json={'username': username, 'password': password})
data = response.json()
access_token = data['data']['token']

# 2. Create a new chat session
response = requests.post(base_url + 'v1/chat/create', json={
    "chat_model": 'gemini-2.0-flash', # If you want only text2sql mode, set this to None
    "text2sql_model": "gemini-2.0-flash",
    "mode": "chat" # If you want only text2sql mode, set this to 'sql'
}, headers={
    "Authorization": f"Bearer {access_token}"
})
data = response.json()
session_id = data['data']['id']

# 3. Start chatting
query = 'ROAA of banking industry from 2016 to 2023'
stream = False
response = requests.post(base_url + 'v1/chat/' + session_id + '/query', json={
    "query": query,
    "stream": stream
}, stream=stream, headers={
    "Authorization": f"Bearer {access_token}"
})

result = response.text
if stream:
    for line in response.iter_lines():
        if line:
            result += line.decode("utf-8")
            print(line.decode("utf-8"))
else:
    print(result)

# 4. Check history
response = requests.get(base_url + 'v1/chat/' + session_id + '/reasoning',
headers={
    "Authorization": f"Bearer {access_token}"
})
print(response.json())