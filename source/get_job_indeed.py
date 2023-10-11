from offres_emploi.utils import filters_to_df, dt_to_str_iso
from offres_emploi import Api
import csv, re
import pprint

import datetime

client = Api(
 
            client_id="PAR_fastjob_1a94967fcf267f1c8adebb94c8f1a8a956b826d561f9ab4d56212a686d5fc3a4", 
            client_secret="7f7baf471ad81b3691041ccafdd5c854c7c4d632a9190990b85891b88dcdd70a"

             )



end_dt = datetime.datetime.today()
start_dt = end_dt - datetime.timedelta(days=60)

param={
        'minCreationDate': dt_to_str_iso(start_dt),
        'maxCreationDate': dt_to_str_iso(end_dt),
        'pays' : 'France',
        'range' : 'O-149'
      }


# Liste pour stocker toutes les offres
all_results = []

# Le chemin vers le fichier CSV dans lequel vous souhaitez enregistrer les données
fichier_csv = "resultats.csv"

# Ouvrir le fichier CSV en mode écriture
with open(fichier_csv, mode="w", newline="", encoding="utf-8") as fichier:
    # Créer un objet CSV Writer
    writer = csv.writer(fichier)

    # Écrire les en-têtes de colonne
    writer.writerow([
        "appellationlibelle",
        "codeNAF",
        "competences",
        "contact",
        "dateActualisation",
        "dateCreation",
        "deplacementCode",
        "deplacementLibelle",
        "description",
        "dureeTravailLibelle",
        "dureeTravailLibelleConverti",
        "entreprise",
        "experienceExige",
        "experienceLibelle",
        "formations",
        "id",
        "intitule",
        "lieuTravail",
        "natureContrat",
        "nombrePostes",
        "offresManqueCandidats",
        "origineOffre",
        "qualificationCode",
        "qualificationLibelle",
        "romeCode",
        "romeLibelle",
        "salaire",
        "secteurActivite",
        "secteurActiviteLibelle",
        "typeContrat",
        "typeContratLibelle"
    ])
    
    
# Pagination en ajustant le paramètre "range" dynamiquement
for offset in range(0, 1150, 150):
    # Générer la valeur pour le paramètre "range" dynamiquement
    range_value = f"{offset}-{offset + 149}"
    param["range"] = range_value

    # Effectuer une recherche
    search_results = client.search(params=param)

    # Récupérer les résultats de la page actuelle
    results = search_results.get("resultats", [])

    # Si aucune offre n'est trouvée sur la page, arrêtez la pagination
    if not results:
        break

    # Ajouter les résultats de la page actuelle à la liste générale
    all_results.extend(results)

    # Enregistrer les résultats de la page actuelle dans le fichier CSV
    with open(fichier_csv, mode="a", newline="", encoding="utf-8") as fichier:
        writer = csv.writer(fichier)
        for resultat in results:
            writer.writerow([
                resultat.get("appellationlibelle", ""),
                resultat.get("codeNAF", ""),
                ", ".join([competence["libelle"] for competence in resultat.get("competences", [])]),
                resultat.get("contact", ""),
                resultat.get("dateActualisation", ""),
                resultat.get("dateCreation", ""),
                resultat.get("deplacementCode", ""),
                resultat.get("deplacementLibelle", ""),
                resultat.get("description", ""),
                resultat.get("dureeTravailLibelle", ""),
                resultat.get("dureeTravailLibelleConverti", ""),
                resultat.get("entreprise", ""),
                resultat.get("experienceExige", ""),
                resultat.get("experienceLibelle", ""),
                ", ".join([formation["niveauLibelle"] for formation in resultat.get("formations", [])]),
                resultat.get("id", ""),
                resultat.get("intitule", ""),
                resultat.get("lieuTravail", {}).get("libelle", ""),
                resultat.get("natureContrat", ""),
                resultat.get("nombrePostes", ""),
                resultat.get("offresManqueCandidats", ""),
                resultat.get("origineOffre", ""),
                resultat.get("qualificationCode", ""),
                resultat.get("qualificationLibelle", ""),
                resultat.get("romeCode", ""),
                resultat.get("romeLibelle", ""),
                resultat.get("salaire", {}).get("libelle", ""),
                resultat.get("secteurActivite", ""),
                resultat.get("secteurActiviteLibelle", ""),
                resultat.get("typeContrat", ""),
                resultat.get("typeContratLibelle", "")
            ])

print(f"Les résultats ont été enregistrés dans {fichier_csv}")

with open(fichier_csv, mode="r", newline="", encoding="utf-8") as fichier:
    # Créer un objet CSV Reader
    reader = csv.reader(fichier)

    # Ignorer la première ligne (en-têtes de colonne)
    next(reader)

    # Compter le nombre d'offres
    nombre_offres = sum(1 for _ in reader)

print(f"Nombre d'offres dans {fichier_csv}: {nombre_offres}")