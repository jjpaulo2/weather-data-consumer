from pydantic import BaseModel


class AuthLoginSchema(BaseModel):
    user: str
    password: str
    keep_connected: bool
    