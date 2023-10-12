import pandas as pd
from offres_emploi.utils import filters_to_df, dt_to_str_iso
from offres_emploi import Api
import datetime

client = Api(
    client_id="PAR_fastjob_1a94967fcf267f1c8adebb94c8f1a8a956b826d561f9ab4d56212a686d5fc3a4",
    client_secret="7f7baf471ad81b3691041ccafdd5c854c7c4d632a9190990b85891b88dcdd70a"
)
end_dt = datetime.datetime.today()
start_dt = end_dt - datetime.timedelta(days=60)

# Paramètres de la requête
param = {
    'minCreationDate': dt_to_str_iso(start_dt),
    'maxCreationDate': dt_to_str_iso(end_dt),
    'pays': 'France',
    'range': 'O-149'
}
all_results = []

offset = 0
total_offres = None

for offset in range(0, 1150, 150):
    param["range"] = f"{offset}-{offset + 149}"
    search_results = client.search(params=param)
    results = search_results.get("resultats", [])

    if not results:
        break

    all_results.extend(results)
    offset += len(results)

    if total_offres is None:
        total_offres = search_results.get("totalResults", 0)

df = pd.DataFrame(all_results)
fichier_csv = "result.csv"
df['dateActualisation'] = pd.to_datetime(df['dateActualisation']).dt.tz_convert(None)
df['dateCreation'] = pd.to_datetime(df['dateCreation']).dt.tz_convert(None)

types_de_donnees = {
    "dateCreation": pd.to_datetime,  # Convertir en type datetime
    "dateActualisation": pd.to_datetime,  # Convertir en type datetime
    "experienceExige": bool,
    "alternance": bool,
    "nombrePostes": int,
    "accessibleTH": bool,
    "offresManqueCandidats": bool
}
for colonne, type_de_donnees in types_de_donnees.items():
    df[colonne] = df[colonne].apply(type_de_donnees)

df['description'] = df['description'].str.replace(',', '').str.replace('\n', '').str.strip()
df.to_csv(fichier_csv, sep=";", index=True, encoding="utf-8")

nombre_offres = len(df)
print(f"Nombre d'offres dans {fichier_csv}: {nombre_offres}")
