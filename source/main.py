import requests
from bs4 import BeautifulSoup
import csv

# URL de la page d'accueil d'Indeed
url = "https://fr.indeed.com/"

# Faites une requête GET à la page d'accueil
response = requests.get(url)

# Vérifiez que la requête s'est bien passée
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Sélectionnez les éléments HTML contenant les offres d'emploi
    job_elements = soup.find_all("div", class_="jobsearch-SerpJobCard")

    # Créez un fichier CSV pour stocker les données
    with open("offres_emploi_indeed.csv", mode="w", newline="") as csv_file:
        fieldnames = ["Titre", "Entreprise", "Lieu", "Salaire", "Description"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Écrivez les en-têtes dans le fichier CSV
        writer.writeheader()

        # Parcourez les éléments d'emploi et extrayez les données
        for job_element in job_elements:
            titre = job_element.find("h2", class_="title").text.strip()
            entreprise = job_element.find("span", class_="company").text.strip()
            lieu = job_element.find("span", class_="location").text.strip()
            salaire = job_element.find("span", class_="salaryText")
            salaire = salaire.text.strip() if salaire else "N/A"
            description = job_element.find("div", class_="summary").text.strip()

            # Écrivez les données dans le fichier CSV
            writer.writerow({"Titre": titre, "Entreprise": entreprise, "Lieu": lieu, "Salaire": salaire, "Description": description})

    print("Les offres d'emploi ont été extraites avec succès et stockées dans offres_emploi_indeed.csv.")
else:
    print("Erreur lors de la requête HTTP.")
