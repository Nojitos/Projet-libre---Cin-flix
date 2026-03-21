from flask import Flask, render_template

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
print(os.getenv("TOKEN"))

client = MongoClient(os.getenv('TOKEN'))
db = client[os.getenv('DB_NAME')]

# Collections contenta email et mot de passe
account = db['account']

# Création de l'app
app = Flask(__name__)

@app.route("/")
def index():
    films = [{
        "poster": "/static/spiderman.jpg",
        "titre": "Harry Potter",
        "realisateur": "chai pas",
        "date": "non plus"
    }]
    return render_template("index.html", films=films)

@app.route("/films")
def films():
    films = [{
        "poster": "{{ url_for('static', filename='harrypotter.png') }}",
        "titre": "Harry Potter",
        "realisateur": "Christopher Columbus",
        "date": "2001"
    },{
        "poster": "{{ url_for('static', filename='spiderman.jpg') }}",
        "titre": "Spider-Man",
        "realisateur": "Sam Raimi",
        "date": "2002"
    },{
        "poster": "{{ url_for('static', filename='starwars.jpg') }}",
        "titre": "Star Wars",
        "realisateur": "George Lucas",
        "date": "1977"
    },
    ]
    return render_template("films.html", films=films)

@app.route("/series")
def series():
    user_email = "email@exemple.com"
    user = account.find_one({"email": user_email})

    if user:
        print(f"Utilisateur trouvé ! Son mdp est : {user['mdp']}")
    else:
        print("Aucun utilisateur avec cet email.")

    return render_template("series.html")

@app.route("/tendances")
def tendances():
    return render_template("tendances.html")

@app.route("/connexion")
def connexion():
    return render_template("connexion.html")

@app.route("/creer-compte")
def creer_compte():
    return render_template("createaccount.html")

@app.route("/exemplefilm")
def exemplefilm():
    return render_template("exemplefilm.html")

# Gestion de l'erreur 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

#Gestion exemple Film
@app.route("/exemple_film/<int:id>")
def film(id):

    popular_reviews = Review.query.filter_by(film_id=id)\
        .order_by(Review.likes.desc())\
        .limit(3).all()

    recent_reviews = Review.query.filter_by(film_id=id)\
        .order_by(Review.created_at.desc())\
        .limit(3).all()

    return render_template(
        "film.html",
        popular_reviews=popular_reviews,
        recent_reviews=recent_reviews
    )

if __name__ == "__main__":
    app.run(debug=True, port=5000)