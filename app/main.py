# Reference Video Link: https://www.freecodecamp.org/news/creating-apis-with-python-free-19-hour-course/
## youtube link: https://www.youtube.com/watch?v=0sOvCWFmrtA
# NOTE: Connect back to venv "source venv/bin/activate" and check that the command pallette is set to venv:venv as well
## 
from fastapi import FastAPI
from app import models
from .database import engine
from app.routers import user, post, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
#from starlette.middleware.cors import CORSMiddleware

print(settings.database_username)

#models.Base.metadata.create_all(bind=engine)

# SET GLOBAL VARIABLE "app"
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)



# SET GLOBAL VARIABLE "my_posts"
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# DEFINE "find_post" FUNCTION
def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p 

# DEFINE "find_index_post" FUNCTION
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i




# GET REQUEST
@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}



