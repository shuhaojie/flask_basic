import requests

BASE_URL = "http://localhost:5001"  # 你的接口服务地址


def test_ping():
    response = requests.get(f"{BASE_URL}/api/user/get_users")
    assert response.status_code == 200


def test_register():
    response = requests.post(url=f"{BASE_URL}/api/user/register",
                             json={"username": "yuwen",
                                   "password": "123456",
                                   "email": "yuwen@qq.com"})
    assert response.status_code == 200


def test_login():
    response = requests.post(url=f"{BASE_URL}/api/user/login",
                             json={"username": "haojie",
                                   "password": "123456",
                                   })
    assert response.status_code == 200


def test_protected_with_token():
    response = requests.post(url=f"{BASE_URL}/api/user/login",
                             json={"username": "haojie",
                                   "password": "123456",
                                   })
    res_json = response.json()
    access_token = res_json["access_token"]
    response = requests.get(url=f"{BASE_URL}/api/user/protected",
                            headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200


def test_protected_without_token():
    response = requests.post(url=f"{BASE_URL}/api/user/login",
                             json={"username": "haojie",
                                   "password": "123456",
                                   })
    res_json = response.json()
    response = requests.get(url=f"{BASE_URL}/api/user/protected")
    assert response.status_code == 200


def test_get_users_for_non_admin():
    response = requests.post(url=f"{BASE_URL}/api/user/login",
                             json={"username": "yuwen",
                                   "password": "123456",
                                   })
    res_json = response.json()

    response = requests.get(url=f"{BASE_URL}/api/user/get_users",
                            headers={"Authorization": f"Bearer {res_json['access_token']}"})
    assert response.status_code == 200


def test_get_users_for__admin():
    response = requests.post(url=f"{BASE_URL}/api/user/login",
                             json={"username": "haojie",
                                   "password": "123456",
                                   })
    res_json = response.json()

    response = requests.get(url=f"{BASE_URL}/api/user/get_users",
                            headers={"Authorization": f"Bearer {res_json['access_token']}"})
    assert response.status_code == 200
