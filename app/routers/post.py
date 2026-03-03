from fastapi import status, HTTPException,Response,APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func # func for count(*)
from typing import  List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)
@router.get("/",response_model=List[schemas.PostOut]) # read # response_model=schemas.Post without this unorder its show how request response send and List cause here multiple list and its try to store in one individual post so we need to give type list for store all list in one list using module typing import optional List
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),limit: int = 10, skip: int = 0,search: Optional[str] = ""):


    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all() ##isouter true cause by dfault left join is left outer join, #.labe mens as or rename
    
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() # if we want post to private
    return  posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) #create
async def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    ## replace=**post.dict() to**post.model_dump()
    new_post = models.Post(owner_id=current_user.id,**post.model_dump()) #### title=post.title, content=post.content, published=post.published or easy way to do this (**post.dict() which mens **post.dict return "title","content" all values from keys its tupel unpacking ### just because we need only titel content or values not keys its give we only all value at for each key)
    db.add(new_post) # add need 
    db.commit() # conn.commit() save
    db.refresh(new_post) # returning *
    return  new_post # return on postman

@router.get("/{id}",response_model=schemas.PostOut) # read for specific id get("/post/{id}") called path parameter
async def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.id == id).first() #first = fetchone
    
    if not post: # use this or use if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found") ### AND 401 for unauthorized
    # if post.owner_id != current_user.id: # if we want post to private
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    return  post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT) # no content
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: # use this or use if not index # need to post.first() select outside for update delete
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    ### AND 401 for unauthorized
    post_query.delete(synchronize_session=False) #synchronize_session=False when perform update delete operations
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first() # need this to select define post_query.first() in outside the query
    if post == None: # use this or use if not index
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action") ### AND 401 for unauthorized
                                  ###updated_post.dict()to updated_post.model_dump()
    post_query.update(updated_post.model_dump(), synchronize_session=False) # post convert to dict its work only with pydantic model not sql model(here no need to unpaking or(**post.dict()) or or value or "title" here need we need key value or tile="title" )
    db.commit()
    return  post_query.first()

