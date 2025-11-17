from app.clients import bp
from app import db
from app.models import Client, Firm
from flask import jsonify, request
from app.helper import ImportCaseHelper, IntegrationHelper
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

    data = request.get_json()

    firm = Firm(data.get("firm_id", 1))
    result = ImportCaseHelper.import_client_handler(
        session=db.session,
        firm=firm,
        row={},
        field_names=data,
        integration_type=IntegrationHelper.CSV_IMPORT,
        integration_id=data.get("integration_id", None),
        matter_id="123456",
        integration_response_object=None,
        create_new_client=True,
        validation=False,
    )
    if error_message := result["row"].get("error_message", None):
        return {"status": "error", "errors": error_message}
    return {"status": "success", "result": result["row"].get("success_msg")}