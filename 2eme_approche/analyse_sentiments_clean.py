from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import csv
import spacy
import pandas as pd
import sys

# Ce code est utilisé pour analyser le ton de l'artcile si celui-ci est en lien avec le changement climatique. 
# Pour des raisons de puissance de calculs par rapport à la tailles de la base de données, nous appliquons cela uniquement sur les titres des articles.

csv.field_size_limit(sys.maxsize)

nlp = spacy.load("en_core_web_sm")

# Le modèle étant limité à des textes de 512 tokens, on tronque les textes plus longs.
def tronquer_texte(texte, max_tokens=512):
    doc = nlp(texte)
    if len(doc) > max_tokens:
        texte_tronque = " ".join([token.text for token in doc[:max_tokens]])
        return texte_tronque
    else:
        return texte

# Cette fonction renvoie une liste associant à chaque article de la base le ton de l'article vis-à-vis du changement climatique.
def climate_test_sentences(file):
    model_path = "climate_sentiments/"
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path, max_length=512)
    pipeline_model = pipeline("text-classification", model=model, tokenizer=tokenizer, batch_size=512, device=0)
    l = []
    with open(file, mode='r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        for j, row in enumerate(reader):
            if row['climate_related'] == 'no':
                l.append('no')
                continue
            title = row['title']
            title = tronquer_texte(title)
            logits = pipeline_model(title)
            l.append(logits[0]['label'])
    return l

# Fonction pour copier un fichier csv
def copy(input_file, output_file):
    df = pd.read_csv(input_file)    
    df.to_csv(output_file, index=False)

# Fonction pour ajouter la liste au fichier csv
def csv_list(lst, csv_file, column_name):
    df = pd.read_csv(csv_file)
    df[column_name] = lst
    df.to_csv(csv_file, index=False)

# On applique ces fonctions pour analyser notre base de données. On a divisé notre base de données en plusieurs fichiers pour des raisons de mémoire.
# On ajoute les print pour suivre l'évolution de l'éxécution du code.

for j in range(1, 3):
    l = climate_test_sentences(f'all-the-news-2-1_1_{j}_climate.csv')
    copy(f'all-the-news-2-1_1_{j}_climate.csv', f'all-the-news-2-1_1_{j}_climate_v2.csv')
    csv_list(l, f'all-the-news-2-1_1_{j}_climate_v2.csv', 'sentiment')
    print(f"Done {j}.")

for i in range(3, 6):
    for j in range(1, 3):
        l = climate_test_sentences(f'all-the-news-2-1_1_{i}_{j}_climate.csv')
        copy(f'all-the-news-2-1_1_{i}_{j}_climate.csv', f'all-the-news-2-1_1_{i}_{j}_climate_v2.csv')
        csv_list(l, f'all-the-news-2-1_1_{i}_{j}_climate_v2.csv', 'sentiment')
        print(f"Done {i} - {j}.")

for i in range (2, 12):
    for j in range (1, 11):
        l = climate_test_sentences(f'all-the-news-2-1_{i}_{j}_climate.csv')
        copy(f'all-the-news-2-1_{i}_{j}_climate.csv', f'all-the-news-2-1_{i}_{j}_climate_v2.csv')
        csv_list(l, f'all-the-news-2-1_{i}_{j}_climate_v2.csv', 'sentiment')
        print(f"Done {i} - {j}.")
