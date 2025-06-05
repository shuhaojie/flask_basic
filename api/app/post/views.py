from api.app.post.routes import post_bp
from flask import jsonify, request, current_app
from api.app.post.models import Post
from api import db


@post_bp.route('/create_post', methods=['POST'])
def create_post():
    """创建新文章"""
    current_app.logger.info("This is a test")
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
