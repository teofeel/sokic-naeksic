from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return ("<p> hello teammates, please implement me </p>"
            "🥺"
            "<p>👉👈</p>")


if __name__ == "__main__":
    app.run(debug=True)
