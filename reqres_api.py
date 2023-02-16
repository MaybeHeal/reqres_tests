import requests


def get_request(url):
    return requests.get(f'https://reqres.in{url}')


def post_request(url, data):
    return requests.post(f'https://reqres.in{url}', data=data)


def put_request(url, data):
    return requests.put(f'https://reqres.in{url}', data=data)


def patch_request(url, data):
    return requests.patch(f'https://reqres.in{url}', data=data)


def delete_request(url):
    return requests.delete(f'https://reqres.in{url}')
