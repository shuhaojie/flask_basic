from flask import Blueprint, jsonify, request
from app.user.models import User, Post
from app.database import db

# 创建API蓝图
api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def home():
    """健康检查端点"""
    return jsonify({"status": "running", "version": "1.0"})


@api_bp.route('/users', methods=['GET'])
def get_users():
    """获取所有用户"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@api_bp.route('/users', methods=['POST'])
def create_user():
    """创建新用户"""
    data = request.get_json()
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@api_bp.route('/posts', methods=['POST'])
def create_post():
    """创建新文章"""
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data or 'user_id' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    post = Post(
        title=data['title'],
        content=data['content'],
        user_id=data['user_id']
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({
        "id": post.id,
        "title": post.title,
        "user_id": post.user_id
    }), 201
