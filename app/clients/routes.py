from app.clients import bp
from app import db
from app.models import Client, Firm
from app.services import ClientService
from flask import jsonify, request
from app.schemas import ClientSchema, ClientImportSchema
from marshmallow import ValidationError
from app.utils import flatten_marshmallow_errors


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)


@bp.route('', methods=["GET"])
def get_clients(): 
    clients = Client.query.all()
    result = clients_schema.dump(clients)
    return jsonify({"clients": result})


@bp.route("", methods=["PATCH"])
def patch_client():
    try:
        data = request.get_json()

        
        schema = ClientImportSchema()
        validated_data = schema.load(data)

        firm = Firm(validated_data.get("firm_id", 1))
        service = ClientService()

        # 3. Call the actual handler
        result = service.import_client_handler(
            firm=firm,
            field_names=validated_data["field_names"]
        )

        # Return success with client data
        return jsonify({
            "status": "success",
            "message": result["message"],
            "created": result["created"],
            "client": client_schema.dump(result["client"])
        }), 200

    except ValidationError as err:
        formatted_errors = flatten_marshmallow_errors(err.messages)
        return jsonify({"status": "error", "errors": formatted_errors}), 400
    
    except Exception as e:

        db.session.rollback()
        return jsonify({
            "status": "error",
            "errors": [{
                "field": "general",
                "message": "An unexpected error occurred. Please try again."
            }]
        }), 500