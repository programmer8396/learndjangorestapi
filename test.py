import requests
import json

BASE_URL = "http://127.0.0.1:8000/"
ENPDPOINT = "api/"
def get_resource():
    id = input("Enter ID ")
    res  =requests.get(BASE_URL+ENPDPOINT+str(id))
    print(res.status_code)
    print(res.json())


def get_all():
    res  =requests.get(BASE_URL+ENPDPOINT)
    print(res.status_code)
    print(res.json())


def create_resource():
    new_emp={
        'eno':500,
        'ename': 'Shiva',
        'esal': 1000,
        'eaddr': 'Chennai',
    }
    resp = requests.post(BASE_URL+ENPDPOINT,data=json.dumps(new_emp))
    print(resp.status_code)
    print(resp.json())

def update_resource(id):
    new_emp={
        'esal':7000,
        'eaddr': 'Mumbai'
    }
    resp = requests.put(BASE_URL+ENPDPOINT+str(id)+'/', data=json.dumps(new_emp))
    print(resp.status_code)
    print(resp.json())

    

def delete_resource(id):
    resp = requests.delete  (BASE_URL+ENPDPOINT+str(id)+'/')
    print(resp.status_code)
    print(resp.json())



delete_resource(5)