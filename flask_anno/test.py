import requests
TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}

x=requests.post('http://localhost:5000/api/currentmission', data={'id':1})

requests.get('http://localhost:5000/api/next/1')


print(x.text)