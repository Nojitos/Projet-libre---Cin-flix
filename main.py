from flask import Flask, render_template

# Création de l'app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/films")
def films():
    return render_template("films.html")

@app.route("/series")
def series():
    return render_template("series.html")

@app.route("/tendances")
def tendances():
    return render_template("tendances.html")

@app.route("/connexion")
def connexion():
    return render_template("connexion.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)