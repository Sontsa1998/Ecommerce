import pandas as pd #Import de la bibliotheque de gestion des dataframes
from sqlalchemy import create_engine


#E (Extract)
Category = pd.read_csv('TB_CATEGORIE.csv', delimiter='|') #Dataset Category
Client = pd.read_csv('TB_CLIENT.csv', delimiter='|') #Dataset Client
Details_Vente = pd.read_csv('TB_DETAIL_VENTE.csv', delimiter='|') #Dataset Details vente
Produit = pd.read_csv('TB_PRODUIT.csv', delimiter='|') #Dataset Produit
Sous_Category = pd.read_csv('TB_SOUS_CATEGORIE.csv', delimiter='|') #Dataset Sous category
Type_Client = pd.read_csv('TB_TYPE_CLIENT.csv', delimiter='|') #Dataset Type Client
Vente = pd.read_csv('TB_VENTE.csv', delimiter='|') #Dataset Vente

#T(Transform)
Category = Category.rename(columns={'CD_CATEGORIE': 'cd_categorie', 'LB_CATEGORIE': 'lb_categorie'})
Client.columns = Client.columns.str.lower()
Details_Vente.columns = Details_Vente.columns.str.lower()
Produit.columns = Produit.columns.str.lower()
Sous_Category.columns = Sous_Category.columns.str.lower()
Type_Client.columns = Type_Client.columns.str.lower()
Vente.columns = Vente.columns.str.lower()

#Jointure entre les differentes tables
df_1 = pd.merge(Vente, Client, on='id_client', how='left')
df_2 = pd.merge(df_1, Type_Client, on='cd_type_client', how='left')
df_3 = pd.merge(df_2, Details_Vente, on='id_vente', how='left')
df_4 = pd.merge(df_3, Produit, on='cd_produit', how='left')
df_5 = pd.merge(df_4, Sous_Category, on='cd_sous_categorie', how='left')
df = pd.merge(df_5, Category, on='cd_categorie', how='left')

#Requetes
request1 = df.groupby('lb_type_client')['prix_vente'].sum().sort_values(ascending=True).reset_index(name='Montant_Total_Ventes')
#print(request1)


#L (Load)
def connection():
    engine = create_engine("mssql://Chris_Evan_Noah/Ecommerce?driver=ODBC+DRIVER+17+FOR+SQL+SERVER") 
    return engine.connect()

df.to_sql('Customers', con=connection(), index=False, if_exists='replace')
#print(loading)