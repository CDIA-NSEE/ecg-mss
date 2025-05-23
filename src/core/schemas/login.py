from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str


class MeResponse(BaseModel):
    name: str
    email: str
    created_at: str
