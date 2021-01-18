import requests

if __name__ == '__main__':
    url = 'http://127.0.0.1:8080/user/login'
    d = {'username': 'admin', 'password': 'admin123'}
    r = requests.post(url, data=d)
    print(r.text)