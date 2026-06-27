from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

posts = []

class Post(BaseModel):
    title: str
    content: str
    author: str
    published: bool = False

@app.get("/")
def root():
    return {
        "name": "Blogging Platform",
        "version": "1.0",
    }
## Add a post
@app.post("/posts")
def post_blog(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = len(posts) + 1
    posts.append(post_dict)
    return post_dict

##Get all posts
@app.get("/posts")
def get_posts():
    return posts

##Get a specific post
@app.get("/posts/{post_id}")
def get_blog(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")

##Update a specific post
@app.put("/posts/{post_id}")
def edit_blog(post_id: int, updated_post: Post):
    for post in posts:
        if post["id"] == post_id:
            post["title"] = updated_post.title
            post["content"] = updated_post.content
            post["author"] = updated_post.author
            post["published"] = updated_post.published
            return post
        
    raise HTTPException(status_code = 404, detail = "Post not found")
        

@app.delete("/posts/{post_id}")
def del_blog(post_id: int):
    for post in posts:
        if post["id"] == post_id:
            posts.remove(post)
            return {"message": f"Post {post_id} deleted"}
    raise HTTPException(status_code=404, detail="Post not found")


