from typing import List, Optional
from .. import schemas, models, utils, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func 
from ..database import get_db
from . import auth

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

## GET POST ##
#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#def get_posts():
#    cursor.execute("""SELECT * FROM posts """)
#    posts = cursor.fetchall()

    print(limit)
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join\
    (models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
    filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

## CREATE POST ##
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

## GET POST BY ID ##
@router.get("/{id}", response_model=schemas.PostOut)
#@router.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
#    post = cursor.fetchone()

#    post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join\
    (models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by\
    (models.Post.id).filter(models.Post.id == id).first()
    
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id : {id} was not found")    
    
    return post

## DELETE POST BY ID ## 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#    cursor.execute("""DELETE FROM posts WHERE id = %s returning * """, (str(id),))
#    deleted_post = cursor.fetchone()
#    conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id : {id} was not found")    
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

## UPDATE POST ##
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):   
#    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, (str(id),)))    
#    updated_post = cursor.fetchone()
#    conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"post with id : {id} was not found")   
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action")
    post_query.delete(synchronize_session=False)

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()