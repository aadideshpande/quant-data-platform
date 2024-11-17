from pydantic import BaseModel


class Body(BaseModel):
    sentence: str

