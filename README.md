# TP_ransomware


## Réponses aux questions du TP

### Chiffrement

Question 1 :

L'algorithme de chiffrement utilisé est l'algorithme de chiffrement par flux, qui consiste à chiffrer les données en continu.
Pour un fichier par exemple, cet algorithme le chiffrera de bout en bout en effectuant un XOR avec la dérivation de clé.
Par conséquent, le ficher fera le même nombre d'octets que le fichier original.

Par rapport à l'algorithme de chiffrement par bloc, cet algorithme est assez simple, et les erreurs
engendrées sont faibles voire inexistantes.

Cet algorithme XOR n'est pas des plus robustes car le fait de répéter la clé sur un fichier de longueur très supérieure à celle de la clé,
laisse l'opportunité de craquer la clé en utilisant la probabilité de répétition des caractères.


### Génération des secrets

Question 2 :

Hacher directement la clé et le sel n'est pas la meilleure idée, car les fonctions de hachages tels que SHA256 ne sont pas prévues pour faire
de la dérivation de clé.

De même, l'utilisation d'un HMAC n'est pas mieux que la proposition précédente en termes de dérivation de clé, car son utilisation ajoute
les atouts d'authenticité et d'intégrité des données.

L'iteret ici avec la fonction de dérivation PBKDF2, est donc d'utiliser une fonction de dérivation appropriée qui inclue ses avantages propres,
comme par exemple, la protection contre les attaques brute-force.


### Enrollement

### Setup

Question 3 :

Il faut préalablement vérifier qu'il n'y ai pas déjà un fichier token.bin, si c'est le cas, cela signifie que le ransomware a déjà chiffré
certains fichiers de la machine cible. Ecraser le fichier token.bin posera problème lors de la demande de récupération de la clé auprès du CNC.

Si un fichier binaire est déjà présent, il faut que le ransomware le conserve et le réutilise pour eviter d'écraser et de faire des doublons.


### Vérifier et utiliser la clé

Question 4 :

On vérifie que la clé est bonne en dérivant la paire clé-sel. Si on retrouve le token, la clé est valide et le déchiffrement peut être
effectué, sinon on attend une nouvelle clé.


