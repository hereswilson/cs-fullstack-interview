from app import db 


class Firm:
    def __init__(self, id, is_corporate=False):
        self.id = id
        self.is_corporate = is_corporate
        self.integration_settings = {
            "update_client_missing_data": True,
            "sync_client_contact_info": True,
        }


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firm_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    birth_date = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), unique=True)
    cell_phone = db.Column(db.String(32))
    integration_id = db.Column(db.String(128), nullable=False)
    ssn = db.Column(db.String(128), nullable=True)