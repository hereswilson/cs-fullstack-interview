from app import db
from app.models import Client, User

class ClientRepository:
    def __init__(self, session):
        self.session = session

    def find_by_integration_id(self, firm_id, integration_id):
        return (
            self.session.query(Client)
            .filter_by(firm_id=firm_id, integration_id=integration_id)
            .first()
        )

    def find_by_email_address(self, email_address, firm_id):
        return (
            self.session.query(Client)
            .filter_by(email=email_address, firm_id=firm_id)
            .first()
        )

    def find_by_phone_number_firm(self, phone_number, firm_id):
        return (
            self.session.query(Client)
            .filter_by(cell_phone=phone_number, firm_id=firm_id)
            .first()
        )

    def save(self, client_instance):
        self.session.add(client_instance)
        return client_instance


class UserRepository:
    def __init__(self, session):
        self.session = session

    def find_by_email_address(self, email_address):
        return self.session.query(User).filter_by(email=email_address).first()