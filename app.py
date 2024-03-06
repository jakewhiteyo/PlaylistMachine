from flask import Flask
from flask_restx import Api
from routes.routes import api_namespace
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

api = Api(app, version="1.0", title="Playlist Machine API", description="This is the API for the Playlist Machine")

api.add_namespace(api_namespace, path="/api")

if __name__ == "__main__":
    print("running")
    app.run(debug=True)