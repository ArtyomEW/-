from pydantic import BaseModel



class CommentsSchema(BaseModel):
    id : int
    post_id: int
    user_email: str
    comment : str

    class Config:
        from_attributes = True


class AddComments(BaseModel):
    comment: str

    class Config:
        from_attributes = True
