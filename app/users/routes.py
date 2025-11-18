from app.clients import bp
from app import db
from app.models import User, Firm
from app.schemas import UserSchema
from flask import jsonify, request

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@bp.route('', methods=["GET"])
def get_users(): 
    users = User.query.all()
    result = users_schema.dump(users)
    return jsonify({"users": result})