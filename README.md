# TP_ransomware


## Réponses aux questions du TP

### Chiffrement

Question 1 : 
L'algorithme de chiffremment utilisé est l'algorithme de chiffrement par flux. Il consiste à chiffrer les données en continue,
pour un fichier par example, cet algorithme le chiffrera de bout-en-bout. En d'autre terme le ficher fera le même nombre d'octet
que le fichier original.

Par rapport à l'algorithme de chiffrement par bloc,cet algorithme est robuste car son fonctionnement assez simple, et les erreurs
engendrées sont faibles voire inexistantes.


### Génération des secrets

Question 2 :



### Enrollement

### Setup

Question 3 :

Il faut préalablement vérifier qu'il n'y ai pas déjà un fichier token.bin, si c'est le cas, cela signifie que le ransomware a déjà chiffré
certains fichiers de la machine cible. Ecraser le fichier token.bin posera problème lors de la phase de récupération de la clé auprès du CNC.

Si un fichier binaire est déjà présent, il faut que le ransomware le conserve et le réutilise pour eviter les doublons.




