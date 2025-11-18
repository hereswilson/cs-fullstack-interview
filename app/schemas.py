from app import ma
from app.models import Client, User 
from marshmallow import fields, validates, ValidationError, validate

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True

class FieldNamesSchema(ma.Schema):
    first_name = fields.String(
        required=True,
        validate=validate.Length(max=128),
        error_messages={"required": "First name is required"}
    )
    last_name = fields.String(
        required=True,
        validate=validate.Length(max=128),
        error_messages={"required": "Last name is required"}
    )
    email = fields.Email(
        allow_none=True,
        validate=validate.Length(max=128)
    )
    phone_numbers = fields.List(
        fields.String(validate=validate.Length(max=32)),
        allow_none=True
    )
    integration_id = fields.String(
        required=True,
        validate=validate.Length(max=128),
        error_messages={"required": "Integration ID is required"}
    )
    birth_date = fields.String(
        allow_none=True,
        validate=validate.Length(max=128)
    )
    ssn = fields.String(
        allow_none=True,
        validate=validate.Length(max=128)
    )
    
    @validates("phone_numbers")
    def validate_phone_numbers(self, value):
        if value and not isinstance(value, list):
            raise ValidationError("phone_numbers must be a list")
        if value and any(not isinstance(num, str) for num in value):
            raise ValidationError("All phone numbers must be strings")

class ClientImportSchema(ma.Schema):
    firm_id = fields.Integer(required=True)
    integration_type = fields.String(
        required=True,
        validate=validate.OneOf(["CSV_IMPORT", "THIRD_PARTY", "MYCASE"])
    )
    field_names = fields.Nested(FieldNamesSchema, required=True)



class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True