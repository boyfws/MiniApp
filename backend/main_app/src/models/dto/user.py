from pydantic import BaseModel

class UserGetByUsername(BaseModel):
    username: str


class UserRequest(BaseModel):
    name: str
    password: bytes
    is_owner: bool

class UserRequestUpdate(BaseModel):
    old_name: str
    new_name: str

class UserResult(BaseModel):
    id: int
