from pydantic import BaseModel




class PostsSchema(BaseModel):
    id: int
    name: str
    description: str
    file_name: str
    user_email: str

    class Config:
        from_attributes = True



class AddPost(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


