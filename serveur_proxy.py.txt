from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
import requests
import os

app = Flask(__name__, static_folder='.', static_url_path='')
auth = HTTPBasicAuth()

# Change tes identifiants ici si besoin
users = {
    "admin": "Sri2677+"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users.get(username) == password:
        return username

@app.route('/')
@auth.login_required
def index():
    # Sert le fichier HTML principal de ton outil
    return app.send_static_file('mo2.html')  # Mets ici le nom exact de ton fichier HTML

@app.route('/proxy')
@auth.login_required
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return 'URL manquante', 400

    print(f"Proxy request to {target_url}")

    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Encoding': 'identity'  # Désactive la compression pour éviter les bugs
    }
    try:
        resp = requests.get(target_url, headers=headers, timeout=30)
        # Supprime l'en-tête Content-Encoding pour Flask/browser
        resp.headers.pop('Content-Encoding', None)
        content_type = resp.headers.get('Content-Type', 'application/json')
        return Response(resp.content, status=resp.status_code, content_type=content_type)
    except Exception as e:
        print(f"Erreur proxy: {e}")
        return f'Erreur lors de la requête proxy: {str(e)}', 500

if __name__ == "__main__":
    # Pour Render, il faut écouter sur 0.0.0.0 et utiliser le port de la variable d'env
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
