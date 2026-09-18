from pydantic import BaseModel


class ChangeRequest(BaseModel):
    change_description: str