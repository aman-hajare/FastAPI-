from fastapi import FastAPI, status, HTTPException,Response, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings
import time


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True # for boolean dataype if not provide by default True
    # rating: int|None = None # int or None by default None if only write int = None(so allow to blank but not allow to write null )

while True:    
    try:
        conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, user=settings.database_username, password=settings.database_password,cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")    
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title":"title of post1", "content":"content of post 1", "id":1}, {"title": "fav foods","content":"I like pizza", "id":2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i       

@app.get("/") # if both path are same ("/") fastapi choose first one ex.here root()
async def root():
    return {"message": "Hello World"}


@app.get("/posts") # read
async def get_posts():
    cursor.execute("""Select * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED) #create
async def create_posts(post: Post):
    new_post = cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title,post.content,post.published))#here (%s,%s,%s) is a variable and after , its value for variable #not use f string cause we need trippel quote """query"""" for sql queries
    new_post = cursor.fetchall()
    conn.commit()
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,100000)
    # my_posts.append(post_dict)
    return {"data": new_post}

# @app.get("/posts/latest") # if we use this method above post id face error cause fast api get latest for get path paramete
# async def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}

@app.get("/posts/{id}") # read for specific id get("/post/{id}") called path parameter
async def get_post(id: str):
    # post = find_post(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id))
    post = cursor.fetchone()
    if not post: # use this or use if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    # index = find_index_post(id)
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id))) # user returning * otherwise face error cause after delete its show nothing 
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post == None: # use this or use if not index
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    # index = find_index_post(id)
    cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id=%s RETURNING *""",(post.title, post.content, post.published, str(id))) # returning * and conn.commit neccesary if we change or post on database (ex,update,delete,create)
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None: # use this or use if not index
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return {"data": updated_post}
