
USE fastjobdb;

-- Table Entreprise
CREATE TABLE Entreprise (
                            entreprise_id INT AUTO_INCREMENT PRIMARY KEY,
                            entrepriseAdaptee BOOLEAN
);


CREATE TABLE OffreEmploi (
                             id INT AUTO_INCREMENT PRIMARY KEY,
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
                             nombrePostes INT,
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
                             complementExercice TEXT,
                             entreprise_id INT,
                             FOREIGN KEY (entreprise_id) REFERENCES Entreprise(entreprise_id)
);



-- Table Salaire
CREATE TABLE Salaire (
                         id INT AUTO_INCREMENT PRIMARY KEY,
                         offre_id INT,
                         libelle VARCHAR(255),
                         FOREIGN KEY (offre_id) REFERENCES OffreEmploi(id)
);


-- Table LieuTravail
CREATE TABLE LieuTravail (
                             id INT AUTO_INCREMENT PRIMARY KEY,
                             offre_id INT,
                             codePostal VARCHAR(10),
                             commune VARCHAR(100),
                             latitude DECIMAL(10, 6),
                             libelle VARCHAR(100),
                             longitude DECIMAL(10, 6),
                             FOREIGN KEY (offre_id) REFERENCES OffreEmploi(id)
);



-- Table OrigineOffre
CREATE TABLE OrigineOffre (
                              id SERIAL PRIMARY KEY,
                              offre_id INT,
                              origine VARCHAR(255),
                              urlOrigine VARCHAR(255),
                              FOREIGN KEY (offre_id) REFERENCES OffreEmploi(id)
);

-- Table Competence
CREATE TABLE Competence (
                            id SERIAL PRIMARY KEY,
                            offre_id INT,
    -- Champs de compétence
                            code VARCHAR(255),
                            exigence VARCHAR(255),
                            libelle VARCHAR(255),
                            FOREIGN KEY (offre_id) REFERENCES OffreEmploi(id)
);

-- Table Formation
CREATE TABLE Formation (
                           id SERIAL PRIMARY KEY,
                           offre_id INT,
    -- Champs de formation
                           exigence VARCHAR(255),
                           niveauLibelle VARCHAR(255),
                           FOREIGN KEY (offre_id) REFERENCES OffreEmploi(id)
);

-- Table Utilisateurs
CREATE TABLE Utilisateurs (
                              id INT AUTO_INCREMENT PRIMARY KEY,
                              Nom VARCHAR(255),
                              Prenom VARCHAR(255),
                              AdresseEmail VARCHAR(255),
                              MotDePasse VARCHAR(255),
                              DateDeNaissance DATE,
                              Telephone VARCHAR(255),
                              Adresse VARCHAR(255),
                              Ville VARCHAR(255),
                              CodePostal VARCHAR(255),
                              Pays VARCHAR(255)
);

-- Table Profils
CREATE TABLE Profils (
                         id VARCHAR(255) PRIMARY KEY,
                         Utilisateur_ID INT,
                         TitreDuProfil VARCHAR(255),
                         Resume TEXT,
                         Experience TEXT, -- Structure de données sérialisée
                         Education TEXT, -- Structure de données sérialisée
                         FOREIGN KEY (Utilisateur_ID) REFERENCES Utilisateurs(id)
);

-- Table Candidatures
CREATE TABLE Candidatures (
                              id SERIAL PRIMARY KEY,
                              Utilisateur_ID INT,
                              OffreEmploi_ID INT,
                              FOREIGN KEY (Utilisateur_ID) REFERENCES Utilisateurs(id),
                              FOREIGN KEY (OffreEmploi_ID) REFERENCES OffreEmploi(id)
);


























/*

Relation entre Utilisateurs et OffreEmploi :
Vous pourriez ajouter une relation entre la table "Utilisateurs" et la table "OffreEmploi"
pour enregistrer les candidatures des utilisateurs à des offres d'emploi.
Dans ce cas, vous auriez une table de liaison, par exemple "Candidatures",
qui enregistrerait les candidatures avec les clés étrangères vers les utilisateurs et les offres d'emploi.

Relation entre OffreEmploi et Entreprise :
Si vous souhaitez suivre quelle entreprise propose une offre d'emploi,
vous pourriez ajouter une relation entre la table "OffreEmploi" et la table "Entreprise" en utilisant la clé étrangère.
Cela permettrait de relier chaque offre à une entreprise.

Relation entre OffreEmploi et Profils :
Si les profils sont liés à des offres d'emploi (par exemple, les profils des recruteurs),
vous pourriez ajouter une relation entre la table "OffreEmploi" et la table "Profils"
pour indiquer quel profil est responsable de chaque offre d'emploi.

Relation entre Utilisateurs et Profils :
Si un utilisateur peut avoir plusieurs profils (par exemple, un profil professionnel et un profil personnel),
vous pourriez ajouter une relation entre la table "Utilisateurs" et la table "Profils" pour permettre à un utilisateur d'avoir plusieurs profils.

*/