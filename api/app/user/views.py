from api.app.user.routes import user_bp
from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from api.app.user.models import User
from api.common.decorators import admin_required
from api import db


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get("username") or not data.get("password") or not data.get("email"):
        current_app.logger.warning("Missing fields")
        return jsonify({"msg": "Missing fields"}), 400

    if User.query.filter_by(username=data["username"]).first():
        current_app.logger.warning("Username already exists")
        return jsonify({"msg": "Username already exists"}), 400

    user = User(username=data["username"],
                email=data["email"],
                is_admin=True if data["username"] == "haojie" else False
                )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered"})


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=user.username,
                                           additional_claims={"is_admin": user.is_admin})
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Invalid credentials"}), 401


@user_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Hello, {current_user}!"})


@user_bp.route('/get_users', methods=['GET'])
@admin_required
def get_users():
    """获取所有用户"""
    current_app.logger.info("This is test")
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@user_bp.route('/create_user', methods=['POST'])
@admin_required
def create_user():
    """创建新用户"""
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
