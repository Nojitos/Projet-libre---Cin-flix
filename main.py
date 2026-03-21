from flask import Flask, render_template

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
        "poster": "/static/harrypotter.jpg",
        "titre": "Harry Potter",
        "realisateur": "Christopher Columbus",
        "date": "2001"
    }]
    return render_template("films.html", films=films)

@app.route("/series")
def series():
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

# Gestion de l'erreur 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)