#===============================================================================
# Titre           : encode.py
# Description     : Ce script est utilise pour obfuscer du code source PHP
# author          : Dream Team
# date            : 20141224
# version         : 0.1     
# usage           : python encode.py
#===============================================================================
import sys
import json
import os
import fnmatch
import zlib
import base64
import shutil
from pprint import pprint

"""
==== TODO
Generer l'extension
Green color for success + Taux de compression
Verifier si le fichier files.json continent des donnees
Verifier aussi si le chemin des fichiers fournis existe
"""

## Algorithm base64
def algobase64( f ):
	
	# Obtenir le code source du fichier et appliquer l'obfuscation
	file = open(f, 'r')

	content = file.read()
	content = content.replace("<?php","")
	content = content.replace("?>","")
	compressed_data = zlib.compress(content)[2:-4]
	content = base64.b64encode(compressed_data)
	file.close()

	# Creation des dossiers si non existant
	if "/" in f:
		dirs = f.split("/");
		path = dirs[-1]
		path = "encoded/" + f.replace(path,"")
		if not os.path.exists(path):
			os.makedirs(path)
		
	# Creation du fichier coder avec un fallback PHP
	file = open("encoded/" + f, 'w+')
	file.write("<?php eval(gzinflate(base64_decode('"+ content +"'))); ?>")
	file.close()
	# TODO: Green color for success + Taux de compression
	print f + " >> encoded/" + f + " = SUCCESS!" 
	return


def obfuscate( f, algo ):
	if algo == "1":
		algobase64(f)
	elif algo == "2":
		print "un autre algo"
	else:
		print "Rien a faire :)"
	return

# Input raw methode de cryptage et demande de cle 
print "Quel algorithme souhaiter vous utiliser pour obscurcir votre code?"
print "1 - Codage Base64"
print "1 - Not implemented yet"
print "1 - Not implemented yet"
algorithm = raw_input("Votre choix? ");

print algorithm
if algorithm != "1":
	sys.exit("Veuillez choissir un algo parmis la liste")

# Supprimer le dossier encoded si existant
if os.path.exists("encoded"):
	shutil.rmtree('encoded')

# TODO : verifier si le fichier files.json continent des donnees
# Verifier aussi si le chemin des fichiers fournis existe

# On cherche les fichiers a obfuscer
json_data=open('files.json')
files = []
extention = ".php"
data = json.load(json_data)
for f in data["fichiers"]:
		if f.endswith("*"):
			f = f[:-1] # Supprimer *
			for root, dirnames, filenames in os.walk(f): # Recherche recursive dans le dossier
  				for filename in fnmatch.filter(filenames, '*' + extention): # On veut seulements les fichiers PHP
					files.append(os.path.join(root, filename))
		else:
			files.append(f)

for f in files:
	obfuscate( f, algorithm )

json_data.close()