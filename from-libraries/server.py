import json
from flask import Flask, request
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

app = Flask(__name__)


para = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())

@app.route('/para', methods=['GET'])
def obtenir_parametres():
    send_para = para.parameter_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.ParameterFormat.PKCS3
    )
    print("Envoie des parametres:", send_para.decode())
    return json.dumps({'para': send_para.decode()})

@app.route('/cle-partagee', methods=['POST'])

def calculer_cle_partagee():
    try:
        
        cle_publique_alice = request.json['cle_publique']
        cle_publique_alice = serialization.load_pem_public_key(cle_publique_alice.encode(), backend=default_backend())

        
        cle_privee_serveur = para.generate_private_key()
        cle_publique_serveur = cle_privee_serveur.public_key()

        cle_partagee = cle_privee_serveur.exchange(cle_publique_alice)

        
        cle_publique_serveur_pem = cle_publique_serveur.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        reponse = {'cle_partagee': cle_partagee.hex(), 'cle_publique_serveur': cle_publique_serveur_pem.decode()}
        print(
        """Clé partagée client-serveur :\n-----BEGIN  CLE PARTAGE -----
        """ + cle_partagee.hex() +"""
        -----END  CLE PARTAGE -----
        """)
        return json.dumps(reponse)
    except Exception as e:
        print("Error:", e)
        return json.dumps({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)

