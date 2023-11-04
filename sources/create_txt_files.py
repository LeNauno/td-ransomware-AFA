"""
=====================================================================================
Ce code permet de créer des fichier .txt dans le conteneur "victime" afin de verifier
le bon fonctionnement du chiffrement.
=====================================================================================
"""

import os

path = '/root/txtFolder'
os.makedirs(path, exist_ok=True)

content = [
    "Contenu du fichier 0\nHello!\n",
    "Contenu du fichier 1\nBonjour !\n",
    "Contenu du fichier 2\nBuenos dias !\n"
]


for i, content in enumerate(content):
    file = f"{path}/file{i}.txt"

    with open(file, "w") as f:
        f.write(content)

    print(f"{file} generated successfully.")
