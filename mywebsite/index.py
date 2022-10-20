from flask import Flask, render_template

app = Flask(__name__)

@app.route("/") #decorador
def index():
    return render_template("index.html")

@app.route("/login") #decorador
def login():
    return render_template("login.html")

@app.route("/register") #decorador
def register():
    return render_template("register.html")

@app.route("/pet") #decorador
def pet():
    return render_template("register_pet.html")

@app.route("/news") #decorador
def news():
    return render_template("news.html")

@app.route("/about") #decorador
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True) #para que se autorefresque
