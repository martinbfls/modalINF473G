import csv

fichier_txt = "Top_pollueurs.txt"

fichier_csv = "Top_pollueurs.csv"

with open(fichier_txt, 'r') as file:
    lignes = file.readlines()

donnees = [ligne.strip().split('\t')[1:] for ligne in lignes]

with open(fichier_csv, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(donnees)

