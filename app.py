from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html', title = 'Home')

@app.route("/about")
def about():
    return render_template('about.html', title = "About")
#örnek olarak yazdım

@app.route("/login", methods = ["GET", "POST"])
def login():
    return "login"

@app.route("/register", methods = ["GET", "POST"])
def register():
    return "register"


if __name__ == "__main__":
    app.run(debug=True)

