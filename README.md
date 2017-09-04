# Grafana OAuth workaround

## Description

If you use Grafana [auth.generic_oauth] adapter and would like to authenticate your users via Microsoft Azure AD, you maybe hit the problem, that Microsoft API don't return a required field "email" in it's json response. To work around the issue we created this small script.

## Usage

Setup a container with the provided dockerfile and point `api_url` in `grafana.ini` to it. The script grabs authentication header and fetches user information from Microsoft API. It extends the respone with a field "email" which has the content from "upn". 
