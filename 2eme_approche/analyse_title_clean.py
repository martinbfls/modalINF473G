import csv
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import pandas as pd
import sys

csv.field_size_limit(sys.maxsize)

# Ce code est utilise pour détéecter, grâce au modèle de CLimateBert, si un article est en lien avec le changement climatique.

# Le modèle étant limité à des textes de 512 tokens, on tronque les textes plus longs. 
# Pour gagner du temps de calculs, on approxime le nombre de tokens.

def tronquer_titre(titre, max_tokens=512, avg_token=4):
    n_char = len(titre)
    estimated_tokens = n_char / avg_token

    if estimated_tokens > max_tokens:
        max_characters = max_tokens * avg_token
        titre_tronquer = titre[:int(max_characters)]
        return titre_tronquer
    else:
        return titre

# Cette fonction renvoie une liste indiquant pour chaque article si il est en lien avec le changement climatique.

def climate_test(file):
    model_path = "climate detector/"
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path, max_length=512)
    titles = []
    rows = []
    with open(file, mode='r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        for i, row in enumerate(reader):
            title = row['title']
            if isinstance(title, str) and len(title) > 0:
                titles.append(tronquer_titre(title))
            else:
                titles.append("N/A")
            rows.append(row)
    pipeline_model = pipeline("text-classification", model=model, tokenizer=tokenizer, batch_size=512)
    logits = pipeline_model(titles)
    return logits

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

for i in range (7, 12):
    for j in range (1, 11):
        logits = climate_test(f'all-the-news-2-1_{i}_{j}.csv')
        copy(f'all-the-news-2-1_{i}_{j}.csv', f'all-the-news-2-1_{i}_{j}_climate.csv')
        csv_list([log['label'] for log in logits], f'all-the-news-2-1_{i}_{j}_climate.csv', 'climate_related')
        print(f"Done {i} - {j}.")
