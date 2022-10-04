from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

app.config.from_prefixed_env()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run()