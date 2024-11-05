from pydantic import BaseModel

class UserDTO(BaseModel):
    user_id: int

class UserResult(BaseModel):
    ...
