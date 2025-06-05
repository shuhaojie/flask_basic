import pytest
from app.server import create_app
from app.user.models import db


@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app('test')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_home_endpoint(client):
    """测试首页端点"""
    response = client.get('/api/')
    assert response.status_code == 200
    assert response.json == {'status': 'running', 'version': '1.0'}


def test_user_creation(client):
    """测试用户创建"""
    response = client.post('/api/users', json={
        'username': 'testuser',
        'email': 'test@example.com'
    })
    assert response.status_code == 201
    assert 'id' in response.json
