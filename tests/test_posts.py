from typing import List
from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res =  authorized_client.get("/posts/") ## res = response
    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    post_list = list(posts_map)
    assert len(res.json()) == len(test_posts) 
    assert res.status_code == 200
    # assert post_list[0].Post.id == test_posts[0].id

def test_unauthorized_user_get_all_posts(client, test_posts):    
    res = client.get("/posts/")
    assert res.status_code == 401  # cause client not a authorized

def test_unauthorized_user_get_one_posts(client, test_posts):    
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401  # cause client not a authorized

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888") # testing invalid id post
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}") 
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("Awesome Beaches", "awesome new content", True),
    ("Favirote Pizza", "i love pepperoni", False),
    ("Tallest Skyscrapers", "omg wow", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title":title, "content":content, "published":published})
    create_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert create_post.title == title
    assert create_post.content == content
    assert create_post.published == published
    assert create_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client,test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title":"mummas boy", "content":"you are a good boy"})
    create_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert create_post.title == "mummas boy"
    assert create_post.content == "you are a good boy"
    assert create_post.published == True
    assert create_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={"title":"mummas boy", "content":"you are a good boy"})
    assert res.status_code == 401 ### 401 for unauthorized

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/8000")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}") #here posts is users2 and try to delete by user 1(authorize_client)
    assert res.status_code == 403

def test_update_post(authorized_client, test_posts):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_other_user_post(client, test_user, test_user2, test_posts):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[3].id,
    }    
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401 ### 401 for unauthorized

def test_unauthorized_user_update_post(client, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_posts):
    data = {
        "title": "update title",
        "content": "update content",
        "id": test_posts[0].id,
    }
    res = authorized_client.put(f"/posts/8000", json=data)
    assert res.status_code == 404