import mysql.connector

# Remplacez les valeurs suivantes par les informations de votre base de données
host = "localhost"
user = "root"
password = "admin"
database = "fast_jobdb"
local_infile=True  

# Créez une connexion à la base de données
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

cursor = conn.cursor()
table_name='offre_empl'

create_table_query = """
CREATE TABLE offre_empl (
    ids INT AUTO_INCREMENT PRIMARY KEY,
    id varchar(255),
    intitule VARCHAR(255),
    description TEXT,
    dateCreation DATETIME,
    dateActualisation DATETIME,
    lieuTravail VARCHAR(255),
    romeCode VARCHAR(255),
    romeLibelle VARCHAR(255),
    appellationlibelle VARCHAR(255),
    entreprise VARCHAR(255),
    typeContrat VARCHAR(255),
    typeContratLibelle VARCHAR(255),
    natureContrat VARCHAR(255),
    experienceExige VARCHAR(255),
    experienceLibelle VARCHAR(255),
    formations TEXT,
    competences TEXT,
    salaire VARCHAR(255),
    dureeTravailLibelle VARCHAR(255),
    dureeTravailLibelleConverti VARCHAR(255),
    alternance VARCHAR(255),
    contact VARCHAR(255),
    nombrePostes VARCHAR(255),
    accessibleTH VARCHAR(255),
    deplacementCode VARCHAR(255),
    deplacementLibelle VARCHAR(255),
    qualificationCode VARCHAR(255),
    qualificationLibelle VARCHAR(255),
    codeNAF VARCHAR(255),
    secteurActivite VARCHAR(255),
    secteurActiviteLibelle VARCHAR(255),
    qualitesProfessionnelles TEXT,
    origineOffre VARCHAR(255),
    offresManqueCandidats VARCHAR(255),
    permis VARCHAR(255),
    agence VARCHAR(255),
    langues TEXT,
    experienceCommentaire TEXT,
    conditionExercice TEXT,
    complementExercice TEXT
);
"""
check_table_query = f"SELECT 1 FROM {table_name} LIMIT 1;"
try:
        cursor.execute(check_table_query)
        table_exists = True
except mysql.connector.Error as e:
        table_exists = False
print(table_exists)
result = cursor.fetchall()
cursor.nextset()

if table_exists:
        delete_table_query = f"DROP TABLE {table_name};"
        cursor.execute(delete_table_query)
        conn.commit()

        
# Exécutez la commande SQL pour créer la table
cursor.execute(create_table_query)
conn.commit()

# Chargez les données depuis le fichier CSV
load_data_query = """
LOAD DATA LOCAL INFILE './result.csv'
INTO TABLE offre_empl
FIELDS TERMINATED BY ';'
IGNORE 1 LINES;

"""

cursor.execute(load_data_query)
conn.commit()
cursor.close()
conn.close()
