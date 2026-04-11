from flask import Flask, render_template, session, request, url_for, redirect

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt
from flask import abort
from bson.objectid import ObjectId

load_dotenv()

mongo = MongoClient(os.getenv('TOKEN'))
films_collection = mongo.db.film
db_users = mongo.db.account
admin_collection = mongo.db.admin

# Création de l'app
app = Flask(__name__)

app.secret_key = os.getenv("KEY")

def utilisateur():
    """
    Renvoir le nom de l'utilisatuer si il est connecté, None sinon
    """
    #Changer le nom de la clé "utilisateur" par "utilisateur_connecte" pour être plus clair
    if "utilisateur" in session:
        return session["utilisateur"]
    else :
        None

def admin():
    """
    Renvoie True si l'utilisateur est admin, False sinon
    """
    # L'utilisateur doit être connecté et doit faire partie de la collection admin
    if utilisateur() is not None and admin_collection.find_one({"pseudo": utilisateur()}) :
        return True
    return False

@app.route("/")
def index():
    films = [{
        "poster": "/static/poster/hp.jpg",
        "titre": "Harry Potter",
        "realisateur": "Christopher Columbus",
        "date": "2001"
    },{
        "poster": url_for('static', filename='/poster/spiderman.jpg'),
        "titre": "Spider-Man",
        "realisateur": "Sam Raimi",
        "date": "2002"
    },{
        "poster":  url_for('static', filename='/poster/starwars.webp'),
        "titre": "Star Wars",
        "realisateur": "George Lucas",
        "date": "1977"
    },
    {
        "poster":  url_for('static', filename='/poster/interstellar.jpg'),
        "titre": "Interstellar",
        "realisateur": "Christopher Nolan",
        "date": "2014"
    },
    ]
    return render_template("index.html", films=films, utilisateur=utilisateur(), admin=admin())

@app.route("/films")
def films():
    films = [{
        "poster": url_for('static', filename='/poster/hp.jpg'),
        "titre": "Harry Potter",
        "realisateur": "Christopher Columbus",
        "date": "2001"
    },{
        "poster": url_for('static', filename='/poster/spiderman.jpg'),
        "titre": "Spider-Man",
        "realisateur": "Sam Raimi",
        "date": "2002"
    },{
        "poster":  url_for('static', filename='/poster/starwars.webp'),
        "titre": "Star Wars",
        "realisateur": "George Lucas",
        "date": "1977"
    },
    {
        "poster":  url_for('static', filename='/poster/interstellar.jpg'),
        "titre": "Interstellar",
        "realisateur": "Christopher Nolan",
        "date": "2014"
    },
    ]
    return render_template("films.html", films=films, utilisateur=utilisateur(), admin=admin())

@app.route("/series")
def series():
    return render_template("series.html", utilisateur=utilisateur(), admin=admin())

@app.route("/tendances")
def tendances():
    return render_template("tendances.html", utilisateur=utilisateur(), admin=admin())

@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect(url_for("index"))

@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    #On vérifie si la méthode est POST pour traiter le formulaire reçu
    if request.method == 'POST':
        if request.form["pseudo"] == "":
            return render_template('connexion.html', error = "Merci d'entrer un pseudo.", utilisateur=utilisateur(), admin=admin())

        #On récupère la table "pseudo" de notre bdd
        user=db_users.find_one({"pseudo":request.form['pseudo']})
        if user :
            if bcrypt.checkpw(request.form['mdp'].encode('utf-8'), user['mdp']):
                session["utilisateur"] = request.form['pseudo']
                return redirect(url_for('index'))
        return render_template('connexion.html', error = 'Les identifiants ne sont pas reconnus.', utilisateur=utilisateur(), admin=admin())
            
    else :
        return render_template('connexion.html', error=None, utilisateur=utilisateur(), admin=admin())

@app.route("/creer_compte", methods=["GET", "POST"])
def creer_compte():
    if request.method == "GET":
        return render_template("createaccount.html", error=None, utilisateur=utilisateur(), admin=admin())
    else :
        if request.form["pseudo"] == "":
            return render_template('connexion.html', error = "Merci d'entrer un pseudo.", utilisateur=utilisateur(), admin=admin())
        
        # On vérifie que les deux mdp sont les mêmes
        if request.form["mdp"] != request.form["mdp_confirm"]:
            print("Les deux mots de passe doivent être les mêmes !")
            return render_template("createaccount.html", error="Les deux mots de passe doivent être les mêmes !", utilisateur=utilisateur(), admin=admin())
        
        # On vérifie si le pseudo existe déjà
        pseudo = request.form['pseudo']
        user=db_users.find_one({"pseudo":pseudo})
        if user :
            print("Le pseudo est déjà enregistré !")
            return render_template("createaccount.html", error="Le pseudo est déjà enregistré !", utilisateur=utilisateur(), admin=admin())
        
        # On vérifie si le pseudo n'est pas vide
        pseudo = request.form['pseudo']
        if pseudo == "" :
            print("Le pseudo est vide !")
            return render_template("createaccount.html", error="Le pseudo ne doit pas être vide !", utilisateur=utilisateur(), admin=admin())
        
        # On vérifie si le mdp n'est pas vide
        if request.form["mdp"] == "":
            return render_template("createaccount.html", error="Le mot de passe doit contenir des crarctères !", utilisateur=utilisateur(), admin=admin())
        
        # On encode le mdp
        mdp = request.form["mdp"].encode("utf-8")
        chaine_alea = bcrypt.gensalt()
        mdp_encrypt = bcrypt.hashpw(mdp, chaine_alea)

        # On l'ajoute à la bdd
        db_users.insert_one({"pseudo": pseudo, "mdp":mdp_encrypt})

        # On ajoute l'utilisateur à la session
        session["utilisateur"] = request.form['pseudo']

        return redirect(url_for('index'))

@app.route("/film/<id>")
def film_page(id):
    film = films_collection.find_one({"_id": ObjectId(id)})

    if not film:
        abort(404)

    return render_template("exemplefilm.html", film=film, utilisateur=utilisateur(), admin=admin())

@app.route("/testfilm")
def testfilm():
    film = films_collection.find_one()
    return render_template("exemplefilm.html", film=film)

@app.route("/admin")
def admin_route():
    # On ne peut accéder à la page qui si l'utilisateur est connecté et est dans la liste des admins
    if admin() :
        print(db_users.find())
        return render_template("admin.html", db_users=db_users.find(), utilisateur=utilisateur(), admin=admin())
    return redirect(url_for("index"))

@app.route("/creer_compte_admin", methods=["GET", "POST"])
def creer_compte_admin():
    if request.method == "GET":
        return render_template("admin.html", error=None, utilisateur=utilisateur(), admin=admin())
    else :
        
        # On vérifie que les deux mdp sont les mêmes
        if request.form["mdp"] != request.form["mdp_confirm"]:
            print("Les deux mots de passe doivent être les mêmes !")
            return render_template("admin.html", error="Les deux mots de passe doivent être les mêmes !", utilisateur=utilisateur(), admin=admin())
        
        # On vérifie si le pseudo existe déjà
        pseudo = request.form['pseudo']
        user=db_users.find_one({"pseudo":pseudo})
        if user :
            print("Le pseudo est déjà enregistré !")
            return render_template("admin.html", error="Le pseudo est déjà enregistré !", utilisateur=utilisateur(), admin=admin())
        
        # On vérifie si le pseudo n'est pas vide
        pseudo = request.form['pseudo']
        if pseudo == "" :
            print("Le pseudo est vide !")
            return render_template("admin.html", error="Le pseudo ne doit pas être vide !", utilisateur=utilisateur(), admin=admin())
        
        # On vérifie si le mdp n'est pas vide
        if request.form["mdp"] == "":
            return render_template("admin.html", error="Le mot de passe doit contenir des crarctères !", utilisateur=utilisateur(), admin=admin())
        
        # On encode le mdp
        mdp = request.form["mdp"].encode("utf-8")
        chaine_alea = bcrypt.gensalt()
        mdp_encrypt = bcrypt.hashpw(mdp, chaine_alea)

        # On l'ajoute à la bdd
        db_users.insert_one({"pseudo": pseudo, "mdp":mdp_encrypt})

        # On ajoute l'utilisateur à la session
        session["utilisateur"] = request.form['pseudo']

        return redirect(url_for('admin_route'))


@app.route("/delete_user/<string:pseudo>", methods=["POST"])
def delete_user(pseudo):
    if admin():
        db_users.delete_one({"pseudo": pseudo})
    return redirect(url_for("admin_route"))


@app.route("/ajouter")
def ajouter_film():
    return render_template("ajouter_film.html", utilisateur=utilisateur(), admin=admin())

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