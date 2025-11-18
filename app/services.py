from app import db
from app.models import Client, Firm
from app.repositories import ClientRepository, UserRepository
import app.util as util


class ClientService:
    def __init__(self, session=None):
        self.session = session or db.session
        self.client_repo = ClientRepository(self.session)
        self.user_repo = UserRepository(self.session)

    
    def import_client_handler(self, firm, field_names):
    """Create or update a client by integration_id."""
    integration_id = field_names["integration_id"]
    
    # Get first phone from array
    phone_numbers = field_names.get("phone_numbers", [])
    cell_phone = phone_numbers[0] if phone_numbers else None
    
    # Look up existing
    client = self.client_repo.find_by_integration_id(firm.id, integration_id)
    
    if not client:
        # Create new
        client = Client(
            firm_id=firm.id,
            first_name=field_names["first_name"],
            last_name=field_names["last_name"],
            email=field_names.get("email"),
            integration_id=integration_id,
            cell_phone=cell_phone,
            birth_date=field_names.get("birth_date"),
            ssn=util.encrypt_ssn(field_names.get("ssn"))
        )
        created = True
    else:
        # Update existing
        client.first_name = field_names["first_name"]
        client.last_name = field_names["last_name"]
        client.email = field_names.get("email")
        if cell_phone:
            client.cell_phone = cell_phone
        if field_names.get("birth_date"):
            client.birth_date = field_names["birth_date"]
        if field_names.get("ssn"):
            client.ssn = field_names["ssn"]
        created = False
    
    self.client_repo.save(client)
    self.session.commit()
    
    return {
        "client": client,
        "created": created,
        "message": f"Client {'created' if created else 'updated'} successfully"
    }
    
    def get_all_clients(self):
        """Get all clients"""
        return Client.query.all()