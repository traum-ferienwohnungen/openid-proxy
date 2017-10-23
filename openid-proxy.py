#!/usr/bin/env python

from flask import Flask, Response, request
import os
import json
import requests
import urllib
import urlparse
# import urllib.parse


app = Flask(__name__)
app.config['TENANT_ID'] = os.getenv('TENANT_ID')
if not app.config['TENANT_ID']:
    app.config['TENANT_ID'] = 'common'
base_url = os.getenv('MSFT_OAUTH_URL')
if not base_url:
    base_url = 'https://login.microsoftonline.com'
app.config['MSFT_OAUTH_URL'] = base_url


@app.route('/healthz', methods=['GET'])
def health():
    return 'OK!'

@app.route('/oauth2/token', methods=['POST'])
def token():
    token_url = '{}/{}/oauth2/token'.format(
        app.config.get('MSFT_OAUTH_URL'),
        app.config.get('TENANT_ID'))
    app.logger.debug(token_url)

    # Append the client_id and client_secret into the POST data
    body = urlparse.parse_qsl(request.get_data())
    body.append(('client_id', request.authorization['username']))
    body.append(('client_secret', request.authorization['password']))

    resp = requests.request(
        method=request.method,
        url=token_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=urllib.urlencode(body),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

@app.route('/userinfo', methods=['GET'])
def userlist():
    info_url = '{}/{}/openid/userinfo'.format(
        app.config.get('MSFT_OAUTH_URL'),
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
    return (json.dumps(claims), r.status_code, dict(r.headers))


def main():
    app.run(debug=bool(os.getenv('DEBUG', False)), host='0.0.0.0')


if __name__ == '__main__':
    main()
