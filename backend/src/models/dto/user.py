from pydantic import BaseModel

class UserRequest(BaseModel):
    id: int

class UserResult(BaseModel):
    status: int
