from pydantic import BaseModel

class UserGetByUserid(BaseModel):
    userid: int

class UserRequest(BaseModel):
    id: int

class UserResult(BaseModel):
    status: int
