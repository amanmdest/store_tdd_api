from pydantic import BaseModel


class BaseSchemaMixIn(BaseModel):
    class Config:
        from_attributes = True
