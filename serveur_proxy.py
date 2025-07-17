from flask import Flask, send_from_directory, request
from flask_httpauth import HTTPBasicAuth
import requests

# Initialisation simple de Flask
app = Flask(__name__)
auth = HTTPBasicAuth()

# --- Vos identifiants de connexion ---
users = {
    "admin": "un_mot_de_passe_tres_secret" 
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# --- Route principale qui sert le fichier HTML ---
@app.route('/')
@auth.login_required
def index():
    # On dit à Flask de chercher 'mo2.html' dans le dossier courant '.'
    return send_from_directory('.', 'mo2.html')

# --- Route pour le proxy API ---
@app.route('/proxy')
@auth.login_required
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return 'URL manquante', 400

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(target_url, headers=headers)

    # On transmet la réponse de l'API telle quelle
    return response.content, response.status_code, response.headers.items()
