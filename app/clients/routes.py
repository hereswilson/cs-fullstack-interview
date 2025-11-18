from app.clients import bp
from app import db
from app.models import Client, Firm
from flask import jsonify, request
from app.schemas import ClientSchema


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

        firm = Firm(data.get("firm_id", 1))
         # Validate payload structure and content
        is_valid, errors = validate_patch_payload(data)
        if not is_valid:
            return jsonify({"status": "error", "errors": errors}), 400

        # Simplified upsert for CSV_IMPORT
        result = upsert_client_simple(
            firm_id=data["firm_id"],
            field_names=data["field_names"]
        )

        # Return success with client data
        return jsonify({
            "status": "success",
            "message": result["message"],
            "created": result["created"],
            "client": client_schema.dump(result["client"])
        }), 200
    
    except Exception as e:

        db.session.rollback()
        return jsonify({
            "status": "error",
            "errors": [{
                "field": "general",
                "message": "An unexpected error occurred. Please try again."
            }]
        }), 500