from website import create_app
from flask import Flask
from flask import Blueprint, render_template

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    app.config['STATIC_FOLDER'] = 'static'
