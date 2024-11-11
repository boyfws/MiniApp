from pydantic import BaseModel

class UserGetByUsername(BaseModel):
    username: str


class UserRequest(BaseModel):
    id: int
    name: str
    owner: bool

class UserRequestUpdate(BaseModel):
    old_name: str
    new_name: str

class UserResult(BaseModel):
    status: int
