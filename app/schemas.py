from app import ma
from app.models import Client, User 
from marshmallow import fields, validates, ValidationError, validate

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True

class ClientImportSchema(ma.Schema):
    integration_type = fields.String(
        required=True,
        validate=validate.OneOf(["CSV_IMPORT", "THIRD_PARTY", "MYCASE"])
    )



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True