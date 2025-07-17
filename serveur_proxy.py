from flask import Flask, send_from_directory, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'mo2.html')

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(target_url, headers=headers)
    return response.content, response.status_code, response.headers.items()
