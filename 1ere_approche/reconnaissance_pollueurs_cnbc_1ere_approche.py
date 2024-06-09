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

with open('artcles_bruts/clean_cnbc.json') as f:
    data = json.load(f)

articles_with_polluters = {}

cpt = 0

for key in data.keys():
    data_2 = data[key]
    for key_2 in data_2.keys():
        article_data = data_2[key_2]
        article = article_data["article"]
        title = data_2[key_2]["title"]
        if len(article) != 0:
            article = article[0]
            polluters_in_article = []

            # Parcourir les pollueurs et vérifier s'ils sont présents dans le texte de l'article
            for polluter_key, aliases in polluters.items():
                for alias in aliases:
                    if alias in article or polluter_key in article:
                        polluters_in_article.append(polluter_key)
                        break  # Arrêter la recherche une fois qu'un alias est trouvé

            # Si des pollueurs ont été trouvés dans l'article, les ajouter à articles_with_polluters
            if polluters_in_article:
                articles_with_polluters[key] = {key_2: {"title": title, "article": article, "polluters": polluters_in_article}}

with open('cnbc_with_polluters.json', 'w') as output_file:
    json.dump(articles_with_polluters, output_file, indent=4)
