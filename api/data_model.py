from pydantic import BaseModel
from typing import Optional
from api import init

# API Request Models
class LoginRequest(BaseModel):
    username: str
    password: str
    
class CreateChatRequestModel(BaseModel):
    chat_model: Optional[str]
    text2sql_model: str
    mode: str

class ChatRequestModel(BaseModel):
    query: str
    stream: bool

# API Response Models
class Meta(BaseModel):
    code: int
    message: str
    
class ApiResponse(BaseModel):
    meta: Meta
    data: object

# Data Models
class Text2SQLSessionModel():
    def __init__(self, text2sql_model):
        self.text2sql_model = text2sql_model

        self.chatbot = init.initialize(chat_model=None, text2sql_model=text2sql_model)
        self.session_id = str(self.chatbot.uid)

class ChatSessionModel():
    def __init__(self, chat_model, text2sql_model):
        self.chat_model = chat_model
        self.text2sql_model = text2sql_model

        self.chatbot = init.initialize(chat_model=chat_model, text2sql_model=text2sql_model)
        self.session_id = self.chatbot.uid