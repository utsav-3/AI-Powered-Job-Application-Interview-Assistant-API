from fastapi import FastAPI, status,HTTPException
#from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2 

conn = psycopg2.connect(
    database="postgres", 
    user="postgres",
    password = "Utsav",
    host="localhost",
    port='5433'
)
cursor = conn.cursor()
print("Database connected successfully!")



app = FastAPI()

class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str

@app.get("/posts")
def get_posts():

    cursor.execute("SELECT * FROM posts")

    posts = cursor.fetchall()

    return {"posts": posts}
    
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s",
                    (id,)
    )
    post = cursor.fetchone()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    return {"post": post}

#CREATE POST

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):

    cursor.execute(
        """
        INSERT INTO posts (title, content)
        VALUES (%s, %s)
        RETURNING *
        """,
        (post.title, post.content)
    )

    new_post = cursor.fetchone()

    conn.commit()

    return {"post": new_post}

#UPDATE POST 

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(
        """
        UPDATE posts
        SET title = %s,
            content = %s
        WHERE id = %s
        RETURNING *
        """,
        (post.title, post.content, id)
    )

    updated_post = cursor.fetchone()

    if updated_post is None:
        conn.rollback()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    conn.commit()

    return {"post": updated_post}
#DELETE POST 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(
        """
        DELETE FROM posts
        WHERE id = %s
        RETURNING id
        """,
        (id,)
    )

    deleted_post = cursor.fetchone()

    if deleted_post is None:

        conn.rollback()

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    conn.commit()

    return None