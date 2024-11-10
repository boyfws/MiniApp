from pydantic import BaseModel

class UserGetByUsername(BaseModel):
    ...


class UserRequest(BaseModel):
    ...

class UserRequestUpdate(BaseModel):
    ...

class UserResult(BaseModel):
    ...
