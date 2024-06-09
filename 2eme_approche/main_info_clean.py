import pandas

# Une fois les noeuds et les liens obtenus, on sélectionne les noeuds les plus pertinents.
# On procède par type de noeuds, en sélectionnant les noeuds avec le plus haut degré.
# Pour chaque catégorie parmis : ORG, PERSON, LOC, NORP, EVENT, PRODUCT et WORK_OF_ART, 
# on sélectionne les 75% des noeuds les plus pertinents au sein de leur catégorie.

# Leur nombre d'occurences a été calculé par des requête SQL au préalable.

# Exemple pour la catégorie WOA (Work of Art) :

df = pandas.read_csv('/Users/martinbeaufils/Downloads/jpp/woa_article.csv')

sum_loc_count = df['woa_count'].sum()
df['woa_rate'] = df['woa_count'] / sum_loc_count
df_principales = df[df['woa_rate'].cumsum() <= 0.75]
df_principales.to_csv('/Users/martinbeaufils/Downloads/Modal/principales_woa.csv', index=True)