#!/usr/bin/env python3

from flask import Flask, request
import os
import requests


app = Flask(__name__)
app.config['TENANT_ID'] = os.getenv('TENANT_ID')


@app.route('/healthz', methods=['GET'])
def health():
    return 'OK!'


@app.route('/userinfo', methods=['GET'])
def userlist():
    info_url = 'https://login.microsoftonline.com/{}/openid/userinfo'.format(
            app.config.get('TENANT_ID'))
    app.logger.debug(info_url)
    headers = {
        'Authorization': request.headers.get('Authorization'),
    }

    r = requests.get(info_url, headers=headers)
    if r.status_code != 200:
        return (r.content, r.status_code, dict(r.headers))

    claims = r.json()
    if claims.get('email', '') == '':
        claims['email'] = claims.get('upn')
    return (claims, r.status_code, dict(r.headers))


def main():
    app.run(debug=bool(os.getenv('DEBUG', False)), host='0.0.0.0')


if __name__ == '__main__':
    main()
