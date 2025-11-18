from app import ma
from app.models import Client
from marshmallow import fields, validates, ValidationError, validate

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True