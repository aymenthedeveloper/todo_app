import requests


endpoint = "http://127.0.0.1:8000/api/tasks/delete/80"


headers = {"authorization": 'token ca6653189f2b3c061418ee8a577835c7f60cbff8'}


response = requests.delete(endpoint, headers=headers)

print(response)