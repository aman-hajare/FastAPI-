from app import schemas 
import pytest
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/") ### res = response
    # print(res.json().get('message')) 
    assert res.json().get('message') == 'Hello World'
    # assert res.status_code_code == 200

def test_create_user(client): ### here json= mens postman json just we fill in postman data in json formate
    res = client.post("/users/", json={"email":"hello123@gmail.com", "password":"password123"})## use /users/ cause by prefix by default  convert / to  /users/ this.
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

def test_login_user(test_user,client):
    res = client.post("/login", data={"username":test_user['email'], "password":test_user['password']}) #here user data= mens form data in postman we fill for login
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com', 'pass22', 403),
    ('amangemail@gmail.com', 'aman233', 403), # if wrong email or pass return 403
    (None, 'pass4343', 422), #if not provide email or pass api given 422 error
    ('wrongemail@gmail.com', None, 422) # if not provide email or pass api given 422 error
])
def test_incorrect_login(test_user, client,email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get('detail') == 'Invaild Credentials'

