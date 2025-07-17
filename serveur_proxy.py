from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import requests

# On dit à Flask que nos fichiers (comme mo2.html) sont dans le même dossier
app = Flask(__name__, static_folder='.', static_url_path='')
auth = HTTPBasicAuth()

# --- Définissez vos identifiants ici ---
users = {
    "admin": "Sri2677+" 
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users.get(username) == password:
        return username

# --- Protéger l'accès à l'application ---
@app.route('/')
@auth.login_required
def index():
    return app.send_static_file('mo2.html')

# --- Protéger l'accès au proxy ---
@app.route('/proxy')
@auth.login_required
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return 'URL manquante', 400

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(target_url, headers=headers)

    return response.content, response.status_code, response.headers.items()
