
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


response = requests.get('http://127.0.0.1:5000/para')
params_pem = response.json()['para']
para = serialization.load_pem_parameters(params_pem.encode(), backend=default_backend())


cle_privee_alice = para.generate_private_key()
cle_publique_alice = cle_privee_alice.public_key()


cle_publique_alice_pem = cle_publique_alice.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


response = requests.post('http://127.0.0.1:5000/cle-partagee', json={'cle_publique': cle_publique_alice_pem.decode()})
cle_partagee_hex = response.json()['cle_partagee']


cle_publique_serveur_pem = response.json()['cle_publique_serveur']
cle_publique_serveur = serialization.load_pem_public_key(cle_publique_serveur_pem.encode(), backend=default_backend())


cle_partagee_alice = cle_privee_alice.exchange(cle_publique_serveur)


print(
"""Clé partagée côté client :\n\n-----BEGIN alice PRIVATE KEY-----
""" + cle_partagee_alice.hex() + """
-----END alice PRIVATE KEY-----
""")
print(
"""Clé partagée client-serveur :\n-----BEGIN  CLE PARTAGE -----
""" + cle_partagee_alice.hex() +"""
-----END  CLE PARTAGE -----
""")


