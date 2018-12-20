Si vous remarquez que des packages sont manquants, exécutez d'abord cette commande:
	pip install -r ./requirements.txt

commande pour lancer le programme :
	py main.py

commande avec paramètre :
	py main.py (-n | -m | -l | -s | -r) (valeur_paramètre)

paramètres :
	-f	--> nom du fichier de sortie excel	optionnel	valeur par défaut : "encoding_data"
	-n	--> nombre de cas de test à produire	obligatoire	valeur par défaut : 1
	-m	--> message à coder			optionnel	valeur par défaut : aucun
	-l	--> longueur du message	à coder		optionnel	valeur par défaut : aucun
	-s	--> nombre de symbol différent		optionnel	valeur par défaut : aucun
	-r	--> facteur de répétition		optionnel	valeur par défaut : aucun
	-w	--> taille du dictionnaire (LZ77)	optionnel	valeur par défaut : 50

si aucun paramètre n'est défini, les paramètres sont choisis aléatoirement