from pydantic import BaseModel


class UserRequest(BaseModel):
    name: str

class UserRequestUpdate(BaseModel):
    old_name: str
    new_name: str

class UserResult(BaseModel):
    id: int
