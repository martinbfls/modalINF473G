import pandas as pd
import csv
import json

with open('polluters_with_info.json', 'r') as f:
    data = json.load(f)

polluters = {}   #liste des polleurs avec les alias

for key in data.keys():
    polluters[key] = []
    aliases = data[key]["entity_info"]["aliases"]
    if "en" in aliases:
        for alias_info in aliases["en"]:
            polluters[key].append(alias_info["value"])

print(polluters)

csv.field_size_limit(100000000)
articles_with_polluters = {}
num_fichier = 6

for i in range(1, num_fichier+1): 
    df = pd.read_csv(f"all-the-news-2-1_{i}.csv", engine='python')

    cpt = 0
    for index, row in df.iterrows():
        polluters_in_article = []
        article = row['article']
        cpt += 1
        print(cpt)
        if isinstance(article, str) and len(article) > 0:
            for polluter_key, aliases in polluters.items():
                    for alias in aliases:
                        if alias in article or polluter_key in article:
                            polluters_in_article.append(polluter_key)
                            break  # Arrêter la recherche une fois qu'un alias est trouvé

            # Si des pollueurs ont été trouvés dans l'article, les ajouter à articles_with_polluters
                    if polluters_in_article:
                        articles_with_polluters[row['date']] = {row['url']: {"title": row['title'], "article": article, "polluters": polluters_in_article}}

with open('all_the_news_with_polluters.json', 'w') as output_file:
    json.dump(articles_with_polluters, output_file, indent=4)