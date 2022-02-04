from pydantic import BaseModel

class SimpleUser(BaseModel):
    username: str

class User(SimpleUser):
    password: str
    
class SimpleWiki(BaseModel):
    topic: str
    user:  str

class Wiki(SimpleWiki):
    content: str
