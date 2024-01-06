import requests


endpoint = "http://127.0.0.1:8000/api/tasks/create"


headers = {"authorization": 'token ca6653189f2b3c061418ee8a577835c7f60cbff8'}

data = {
    "name": "testing permission"
}

response = requests.post(endpoint, headers=headers, json=data)

print(response.json())