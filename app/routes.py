from app import app, db
from app.models import Client, Firm
from flask import request
from app.helper import ImportCaseHelper, IntegrationHelper

@app.route("/")
def hello():
    return "Hello, Interviewee!"


@app.route("/clients", methods=["GET"])
def get_clients():
    clients = Client.query.all()
    client_list = [
        {
            "id": c.id,
            "firm_id": c.firm_id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "birth_date": c.birth_date,
            "email": c.email,
            "cell_phone": c.cell_phone,
            "integration_id": c.integration_id,
            "ssn": c.ssn,
        }
        for c in clients
    ]
    return {"clients": client_list}


@app.route("/clients", methods=["PATCH"])
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