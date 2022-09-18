from pydantic import BaseModel



class Photo(BaseModel):
    id: str = ''
    description: str = ''
    image: str = ''