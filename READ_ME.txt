Si vous remarquez que des packages sont manquants, ex�cutez d'abord cette commande:
	pip install -r ./requirements.txt

commande pour lancer le programme :
	py main.py

commande avec param�tre :
	py main.py (-n | -m | -l | -s | -r) (valeur_param�tre)

param�tres :
	-f	--> nom du fichier de sortie excel	optionnel	valeur par d�faut : "encoding_data"
	-n	--> nombre de cas de test � produire	obligatoire	valeur par d�faut : 1
	-m	--> message � coder			optionnel	valeur par d�faut : aucun
	-l	--> longueur du message	� coder		optionnel	valeur par d�faut : aucun
	-s	--> nombre de symbol diff�rent		optionnel	valeur par d�faut : aucun
	-r	--> facteur de r�p�tition		optionnel	valeur par d�faut : aucun
	-w	--> taille du dictionnaire (LZ77)	optionnel	valeur par d�faut : 50

si aucun param�tre n'est d�fini, les param�tres sont choisis al�atoirement