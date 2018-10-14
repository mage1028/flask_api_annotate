import requests
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

x=requests.post('http://localhost:5000/api/mission', data=None)


print(x.text)