import requests

r = requests.post("http://localhost:2808/api/v1/add_progress", json={'mediaId': 15583, 'progress': 8})

print(r.text)