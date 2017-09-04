#!/usr/bin/env python3

from flask import Flask, request
import json
import os
import requests


app = Flask(__name__)


@app.route('/userinfo', methods=['GET'])
def userlist():
    return json.dumps(
        get_claims(request.headers.get('Authorization')))


@app.route('/healthz', methods=['GET'])
def health():
    return 'OK!'


def get_claims(id_token):
    userinfo_endpoint = \
        'https://login.microsoftonline.com/<tenant-id>/openid/userinfo'
    headers = {'Authorization': id_token}
    try:
        request = requests.get(userinfo_endpoint, headers=headers)
        request.raise_for_status()
        claims = request.json()
        claims['email'] = claims.get('upn')
        return claims
    except requests.exceptions.HTTPError as e:
        print(e)
        exit(1)


def main():
    app.run(debug=bool(os.getenv('DEBUG', False)), host='0.0.0.0')


if __name__ == '__main__':
    main()
