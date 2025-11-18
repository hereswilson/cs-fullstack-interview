from app.clients import bp
from app import db
from app.models import Client, Firm
from flask import jsonify, request
from app.schemas import ClientSchema, ClientImportSchema


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
        schema = ClientImportSchema()
        errors = schema.validate(data)
        if errors:
            formatted_errors = [{"field": k, "message": str(v)} for k, v in errors.items()]
            return jsonify({"status": "error", "errors": formatted_errors}), 400

        firm = Firm(data.get("firm_id", 1))
        service = ClientService()

        # 3. Call the actual handler
        result = service.import_client_handler(
            firm=firm,
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