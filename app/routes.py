from app import app, db
from app.models import Client, Firm
from flask import jsonify, request
from app.helper import ImportCaseHelper, IntegrationHelper
from app.schemas import ClientSchema

@app.route("/")
def hello():
    return "Hello, Interviewee!"


