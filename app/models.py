from app import db 
import sqlalchemy as sa
import sqlalchemy.orm as so
from typing import Optional


class Firm:
    def __init__(self, id, is_corporate=False):
        self.id = id
        self.is_corporate = is_corporate
        self.integration_settings = {
            "update_client_missing_data": True,
            "sync_client_contact_info": True,
        }


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True, nullable=False)


class Client(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    firm_id: so.Mapped[int] = so.mapped_column(nullable=False)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    birth_date: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), nullable=True)
    email: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), unique=True, nullable=True)
    cell_phone: so.Mapped[Optional[str]] = so.mapped_column(sa.String(32), nullable=True)
    integration_id: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False)
    ssn: so.Mapped[Optional[str]] = so.mapped_column(sa.String(128), nullable=True)