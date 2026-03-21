from flask import Flask, render_template, session, request, url_for, redirect

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
from flask import abort
from bson.objectid import ObjectId

load_dotenv()

mongo = MongoClient(os.getenv('TOKEN'))
films_collection = mongo.db.account.film

# Création de l'app
app = Flask(__name__)

def utilisateur():
    """
    Renvoir le nom de l'utilisatuer si il est connecté, None sinon
    """
    if "utilisateur" in session:
        return session["utilisateur"]
    else :
        None

@app.route("/")
def index():
    films = [{
        "poster": "/static/spiderman.jpg",
        "titre": "Harry Potter",
        "realisateur": "chai pas",
        "date": "non plus"
    }]
    return render_template("index.html", films=films, utilisateur=utilisateur())

@app.route("/films")
def films():
    films = [{
        "poster": url_for('static', filename='harrypotter.png'),
        "titre": "Harry Potter",
        "realisateur": "Christopher Columbus",
        "date": "2001"
    },{
        "poster": url_for('static', filename='spiderman.jpg'),
        "titre": "Spider-Man",
        "realisateur": "Sam Raimi",
        "date": "2002"
    },{
        "poster":  url_for('static', filename='starwars.jpg'),
        "titre": "Star Wars",
        "realisateur": "George Lucas",
        "date": "1977"
    },
    ]
    return render_template("films.html", films=films, utilisateur=utilisateur())

@app.route("/series")
def series():
    return render_template("series.html", utilisateur=utilisateur())

@app.route("/tendances")
def tendances():
    return render_template("tendances.html", utilisateur=utilisateur())

@app.route("/connexion")
def connexion():
    #On vérifie si la méthode est POST pour traiter le formulaire reçu
    if request.method == 'POST':
        #On récupère la table "email" de notre bdd
        db_users = mongo.db.account
        user=db_users.find_one({"email":request.form['email']})
        if user :
            if bcrypt.checkpw(request.form['mdp'].encode('utf-8'), user['mdp']):
                session["utilisateur"] = request.form['utilisateur']
                return redirect(url_for('index'))
        return render_template('connexion.html', error = 'Les identifiants ne sont pas reconnus.', utilisateur=utilisateur())
            
    else :
        return render_template('connexion.html', error=None, utilisateur=utilisateur())

@app.route("/creer_compte", methods=["GET", "POST"])
def creer_compte():
    if request.method == "GET":
        return render_template("createaccount.html", error=None, utilisateur=utilisateur())
    else :
        # On vérifie que les deux mdp sont les mêmes
        if request.form["mdp"] != request.form["mdp_confirm"]:
            print("Les deux mots de passe doivent être les mêmes !")
            return render_template("createaccount.html", error="Les deux mots de passe doivent être les mêmes !", utilisateur=utilisateur())
        
        # On vérifie si l'email existe déjà
        email = request.form['email']
        db_users = mongo.db.account
        user=db_users.find_one({"email":email})
        if user :
            print("L'email est déjà enregistré !")
            return render_template("createaccount.html", error="L'email est déjà enregistré !", utilisateur=utilisateur())
        
        # On encode le mdp
        mdp = request.form["mdp"].encode("utf-8")
        chaine_alea = bcrypt.gensalt()
        mdp_encrypt = bcrypt.hashpw(mdp, chaine_alea)

        # On l'ajoute à la bdd
        db_users.insert_one({"email": email, "mdp":mdp_encrypt})

        # On ajoute l'utilisateur à la session
        session["utilisateur"] = request.form['utilisateur']

        return redirect(url_for('index'))

@app.route("/film/<id>")
def film_page(id):
    film = films_collection.find_one({"_id": ObjectId(id)})

    if not film:
        abort(404)

    return render_template("exemplefilm.html", film=film, utilisateur=utilisateur())

@app.route("/testfilm")
def testfilm():
    film = films_collection.find_one()
    return str(film)

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