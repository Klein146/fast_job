import pandas as pd
import datetime
import mysql.connector
from sqlalchemy import create_engine
from offres_emploi.utils import dt_to_str_iso
from offres_emploi import Api
def get_api_data():
    client = Api(
        client_id="PAR_fastjob_1a94967fcf267f1c8adebb94c8f1a8a956b826d561f9ab4d56212a686d5fc3a4",
        client_secret="7f7baf471ad81b3691041ccafdd5c854c7c4d632a9190990b85891b88dcdd70a"
    )
    end_dt = datetime.datetime.today()
    start_dt = end_dt - datetime.timedelta(days=60)
    all_results = []
    for offset in range(0, 1150, 150):
        param = {
            'minCreationDate': dt_to_str_iso(start_dt),
            'maxCreationDate': dt_to_str_iso(end_dt),
            'pays': 'France',
            'range': f'{offset}-{offset + 149}'
        }
        search_results = client.search(params=param)
        results = search_results.get("resultats", [])
        if not results:
            break
        all_results.extend(results)
    return pd.DataFrame(all_results)

def clean_data(df):
    df['dateActualisation'] = pd.to_datetime(df['dateActualisation']).dt.tz_convert(None)
    df['dateCreation'] = pd.to_datetime(df['dateCreation']).dt.tz_convert(None)
    types_de_donnees = {
        "dateCreation": pd.to_datetime,
        "dateActualisation": pd.to_datetime,
        "experienceExige": bool,
        "alternance": bool,
        "nombrePostes": int,
        "accessibleTH": bool,
        "offresManqueCandidats": bool
    }
    
    for colonne, type_de_donnees in types_de_donnees.items():
        df[colonne] = df[colonne].apply(type_de_donnees)
    df['description'] = df['description'].str.replace('[,\n]', '').str.strip()
    df = df.applymap(lambda cellule: cellule.replace(';', '') if isinstance(cellule, str) else cellule)
    return df

def main():
    df = get_api_data()
    df = clean_data(df)
    fichier_csv = "result.csv"
    df.to_csv(fichier_csv, sep=";", index=False, encoding="utf-8") 
    print(f"Nombre d'offres dans {fichier_csv}: {len(df)}")
    df = pd.read_csv('result.csv', sep=';', encoding='utf-8')
    config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'fast_jobdb',
    }
    conn = mysql.connector.connect(**config)
    engine = create_engine(f'mysql+mysqlconnector://{config["user"]}:{config["password"]}@{config["host"]}/{config["database"]}')
    df.to_sql('offres_emplois', engine, if_exists='replace', index=False)
    conn.close()
if __name__ == "__main__":
    main()
