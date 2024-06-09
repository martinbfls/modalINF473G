import json
import spacy, csv
from spacy.matcher import Matcher
import sys

csv.field_size_limit(sys.maxsize)

# Ce fichier est utilisé pour construire les noeuds et les arcs du graphe.
# On reprend la construction avec Spacy vue en TD.

# On commence par créer un fichier texte contenant les articles en lien avec le changement climatique.
def create_text(input_file, output_file):
    data = []
    with open(input_file, newline='') as csvfile:
        csv = csv.DictReader(csvfile)
        for ligne in csv:
            article = ligne['article']
            if ligne['climate_related'] == 'yes':
                data.append(article)

    with open(output_file, 'w', encoding='utf-8') as f:
        for article in data:
            if len(article) > 0:
                f.write(article)
                f.write('\n\n')

# Fonction pour construire les noeuds et les arcs
def nodes_construction(input_file, output_file_nodes, output_file_triples):
    nlp = spacy.load("en_core_web_sm")

    matcher = Matcher(nlp.vocab)
    pattern1 = [{"POS": {"IN":["AUX","VERB"]}}, {"POS": "VERB", "OP":"?"}, {"POS": "PART", "OP":"?"},  {"POS": "ADV", "OP":"?"}]
    pattern2 = [{"POS": {"IN":["AUX","VERB"]}}, {"POS": "VERB", "OP":"?"}, {"POS": "PART", "OP":"?"},  {"POS": "ADV", "OP":"?"}, {"POS":{"IN":["ADP","PART"]}, "OP":"?"}]
    pattern3 = [{"POS": {"IN":["AUX","VERB"]}},{"POS": "VERB", "OP":"?"},{"POS":{"IN":["NOUN", "ADJ", "ADV", "PRON", "DET"]}, "OP":"*"},{"POS":{"IN":["ADP","PART"]}}]

    matcher.add("predicate", [pattern1, pattern2, pattern3], greedy='LONGEST')
    nlp.add_pipe("sentencizer")
    rb = open(input_file, encoding="utf-8")
    wb = open(output_file_triples, "w", encoding="utf-8", newline='')
    wb2 = open(output_file_nodes, "w", encoding="utf-8", newline='')
    ids = {}
    count = 0
    writer_triples = csv.DictWriter(wb, fieldnames=['subject', 'predicate','object'])
    writer_nodes = csv.DictWriter(wb2, fieldnames= ['Id', 'Name', 'Type'])
    cpt = 0
    for content in rb.readlines():
        cpt += 1
        if cpt % 1000 == 0:
            print(cpt)
        content = content.split("\t")[0]
        doc = nlp(content)
        for sentence in doc.sents:
            doc = nlp(sentence.text)
            chunk_list = [(chunk.text, chunk.start, chunk.end) for chunk in doc.noun_chunks]
            entities = {}
            for ent in doc.ents:
                entities[ent.text] = ent.label_
            matches = matcher(doc)
            for match_id, start, end in matches:
                span = doc[start:end]
                subject = ("",0,0)
                object = ("",len(sentence),len(sentence))
                for (ctext,cstart,cend) in chunk_list:
                    if cend <= start and cend >=subject[2]:
                        subject = (ctext,cstart,cend)
                    if cstart >= end and cstart <= object[1]:
                        object = (ctext,cstart,cend)
                if len(subject[0]) and subject[0] in entities and len(object[0]) and object[0] in entities:
                    writer_triples.writerow({"subject":subject[0], "predicate":span.text, "object":object[0]})
                    if subject[0] not in ids:
                        ids[subject[0]] = count
                        count += 1
                        writer_nodes.writerow({"Id":str(ids[subject[0]]), "Name":subject[0], "Type": entities[subject[0]]})
                    if object[0] not in ids:
                        ids[object[0]] = count
                        count += 1
                        if object[0] in entities:
                            writer_nodes.writerow({"Id": str(ids[object[0]]), "Name": object[0], "Type": entities[object[0]]})
                        else:
                            writer_nodes.writerow(
                                {"Id": str(ids[object[0]]), "Name": object[0], "Type": "string"})

# Fonction pour créer les fichiers csv correspondant aux noeuds et aux arcs
def create_csv(output_file_nodes, output_file_triples):
    with open(output_file_nodes, mode='w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(['Id', 'Name', 'Type'])
    with open(output_file_triples, mode='w', newline='') as fichier_csv:
        writer = csv.writer(fichier_csv)
        writer.writerow(['subject', 'predicate', 'object'])


# On applique ces fonctions pour construire les noeuds et les arcs de notre base de données.
# On a divisé notre base de données en plusieurs fichiers pour des raisons de mémoire.
# La variable c a été utilisé car on a du s'y reprendre à plusieurs fois comme les codes étaient trop long à s'exécuter et que les ordinateurs plantaient.
# On ajoute les print pour suivre l'évolution de l'éxécution du code.

c = 89
for i in range(8, 11):
    create_text(f'all-the-news-2-1_9_{i}_climate.csv', f'all_the_news_climate_{c}.txt')
    create_csv(f'all_the_news_climate_{c}_nodes.csv', f'all_the_news_climate_{c}_triples.csv')
    nodes_construction(f'all_the_news_climate_{c}.txt', f'all_the_news_climate_{c}_nodes.csv', f'all_the_news_climate_{c}_triples.csv')
    c += 1
    print(f"Done {i}")

for i in range(10, 12):
    for j in range (1, 11):
        create_text(f'all-the-news-2-1_{i}_{j}_climate.csv', f'all_the_news_climate_{c}.txt')
        create_csv(f'all_the_news_climate_{c}_nodes.csv', f'all_the_news_climate_{c}_triples.csv')
        nodes_construction(f'all_the_news_climate_{c}.txt', f'all_the_news_climate_{c}_nodes.csv', f'all_the_news_climate_{c}_triples.csv')
        c += 1
        print(f"Done {i} {j}")
