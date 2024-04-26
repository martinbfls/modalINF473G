import pandas as pd

# Taille de chaque chunk
chunk_size = 10000  

# Lecture du fichier CSV en chunks
chunks = pd.read_csv("all-the-news-2-1.csv", chunksize=chunk_size)

# Parcours et impression des chunks
for chunk in chunks:
    # Impression des éléments de la colonne "article" pour chaque chunk
    print(chunk['article'])

    # Si vous souhaitez limiter l'impression à seulement 10 chunks, vous pouvez ajouter une condition
    # Par exemple, pour limiter l'impression aux 10 premiers chunks :
    # if condition:
    #     break
