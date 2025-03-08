import json
from fastapi import Depends, FastAPI, status
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

import uuid

from api import configuration as config
from api import data_model as model
from api import security
from api.security import validate_token

import uvicorn

# Initialize instances
app = FastAPI()

sessions = {}

# API services
@app.post('/v1/login')
def login(request_data: model.LoginRequest):
    if security.verify_password(username=request_data.username, password=request_data.password):
        token = security.generate_token(request_data.username)
        
        response = model.ApiResponse(meta=model.Meta(code=200, message=''), data={"token": token})
        return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)
    else:
        response = model.ApiResponse(meta=model.Meta(code=404, message=f'User not found'), data={})
        return JSONResponse(response, status_code=status.HTTP_404_NOT_FOUND)

@app.post('/v1/chat/create', dependencies=[Depends(validate_token)])
async def create_chat(body: model.CreateChatRequestModel):

    if (body.chat_model is not None) and (body.chat_model not in config.CHAT_MODELS):
        response = model.ApiResponse(meta=model.Meta(code=400, message=f'The chat model {body.chat_model} is not valid. It must be in {', '.join(config.CHAT_MODELS)}'), data={})
        return JSONResponse(response, status_code=status.HTTP_400_BAD_REQUEST)

    if body.text2sql_model not in config.CHAT_MODELS:
        response = model.ApiResponse(meta=model.Meta(code=400, message=f'The text2sql model {body.text2sql_model} is not valid. It must be in {', '.join(config.TEXT2SQL_MODELS)}'), data={})
        return JSONResponse(response, status_code=status.HTTP_400_BAD_REQUEST)

    chat_model = None

    if body.mode == 'sql':
        chat_model = model.Text2SQLSessionModel(text2sql_model=body.text2sql_model)
    else:
        chat_model = model.ChatSessionModel(chat_model=body.chat_model, text2sql_model=body.text2sql_model)
    
    uid = chat_model.chatbot.uid
    sessions[uid] = chat_model

    response = model.ApiResponse(meta=model.Meta(code=201, message=''), data={"id": uid})
    return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_201_CREATED)

@app.post('/v1/chat/{uid}/query', dependencies=[Depends(validate_token)])
async def chat(uid, body: model.ChatRequestModel):
    if uid not in sessions.keys():
        response = model.ApiResponse(meta=model.Meta(code=400, message=f'The chat id {uid} does not exist'), data={})
        return JSONResponse(content=jsonable_encoder(response))

    session = sessions[uid]

    if body.stream:
        return StreamingResponse(session.chatbot.stream(body.query, version=config.CHAT_VERSION), media_type='text/event-stream')
    else:
        result = ''
        for chunk in session.chatbot.stream(body.query, version=config.CHAT_VERSION):
            if isinstance(chunk, str):
                result += chunk
        
        response = model.ApiResponse(meta=model.Meta(code=200, message=''), data=result)

        return JSONResponse(content=jsonable_encoder(response), status_code=status.HTTP_200_OK)

@app.get('/v1/chat/{uid}/reasoning', dependencies=[Depends(validate_token)])
async def chat(uid):
    if uid not in sessions.keys():
        response = model.ApiResponse(meta=model.Meta(code=400, message=f'The chat id {uid} does not exist'), data={})
        return JSONResponse(content=jsonable_encoder(response))

    with open(f'history/{uid}.json', 'r') as file:
        chat_data = json.load(file)

        response = model.ApiResponse(meta=model.Meta(code=200, message=''), data=chat_data)

        return JSONResponse(content=jsonable_encoder(response))

# Start the server
uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
