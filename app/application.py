from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'  # Remplacez par une clé de votre choix

# Configuration de la base de données
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="fastjobdb"
)

@app.route('/')
def accueil():
    # Affichez ici les offres d'emploi depuis la base de données
    return "Bienvenue sur la page d'accueil"

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # Récupérez les données du formulaire d'inscription
        nom = request.form['Nom']
        prenom = request.form['Prenom']
        email = request.form['AdresseEmail']

        # Insérez l'utilisateur dans la base de données
        cursor = db.cursor()
        cursor.execute("INSERT INTO Utilisateurs (Nom, Prenom, AdresseEmail) VALUES (%s, %s, %s)", (nom, prenom, email))
        db.commit()
        cursor.close()

        # Redirigez l'utilisateur vers la page de connexion
        return redirect(url_for('connexion'))

    return render_template('inscription.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        # Récupérez les données du formulaire de connexion
        email = request.form['AdresseEmail']

        # Vérifiez si l'utilisateur existe dans la base de données
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Utilisateurs WHERE AdresseEmail = %s", (email,))
        utilisateur = cursor.fetchone()
        cursor.close()

        if utilisateur:
            # Stockez l'utilisateur en session (connexion réussie)
            session['utilisateur'] = utilisateur
            return "Connexion réussie"
        else:
            return "Adresse e-mail incorrecte. Veuillez réessayer."

    return render_template('connexion.html')

if __name__ == '__main__':
    app.run(debug=True)

