from website import create_app
from flask import Flask
from flask import Blueprint, render_template

# app = Flask(__name__)


# @app.route('/')
# def home():
#     return render_template("home.html")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    app.config['STATIC_FOLDER'] = 'static'
