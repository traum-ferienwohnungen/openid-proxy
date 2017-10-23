# Grafana OAuth workaround

[![Docker Build Status](https://img.shields.io/docker/build/traumfewo/openid-proxy.svg)](https://hub.docker.com/r/traumfewo/openid-proxy/)

## Description

If you use Grafana `[auth.generic_oauth]` adapter and would like to authenticate your users via Microsoft Azure AD, you maybe hit the problem, that Microsoft API don't return a required field `email` in it's json response (see [grafana/issues/5877](https://github.com/grafana/grafana/issues/5877)).

Maybe you also found an issue where Azure AD requires the `client_id` and `client_secret` fields in the POST body to `/oauth2/token` (you would see something like this in your Grafana logs):
```
AADSTS90014: The request body must contain the following parameter: 'client_id'
```

To work around the issue we created this small script.

## Usage

Setup a container with the provided dockerfile and point `api_url` in `grafana.ini` to it.

```
[auth.generic_oauth]
enabled = true
allow_sign_up = true
client_id = <Application ID>
client_secret = <Application Secret>
scopes = openid,email,profile
auth_url = https://login.microsoftonline.com/<Azure AD tenant ID>/oauth2/authorize
token_url = http://<your-openid-proxy-instance>/oauth2/token
api_url = http://<your-openid-proxy-instance>:5000
```

The script grabs authentication header and fetches user information from Microsoft API. It extends the response with a field `email` using the contents from `upn`.
If you are using it to proxy requests to `/oauth2/token` then it will copy the auth header details into the POST body also.
