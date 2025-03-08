from agent import Chatbot, Text2SQL, ChatbotSematic
from agent.const import (
    ChatConfig,
    Text2SQLConfig,
    GEMINI_FAST_CONFIG,
    GEMINI_FAST_CONFIG_V2,
    GPT4O_MINI_CONFIG,
    GPT4O_CONFIG,
    TEXT2SQL_FAST_GEMINI_CONFIG,
    TEXT2SQL_FAST_OPENAI_CONFIG,
    TEXT2SQL_THINKING_GEMINI_CONFIG,
    TEXT2SQL_4O_CONFIG,
    TEXT2SQL_QWEN25_CODER_3B_SFT_CONFIG,
    TEXT2SQL_QWEN25_CODER_1B_KTO_CONFIG,
    TEXT2SQL_4O_CONFIG,
    TEXT2SQL_QWEN25_CODER_3B_KTO_CONFIG,
    TEXT2SQL_GEMINI_PRO_EXP_CONFIG,
)
from agent.prompt.prompt_controller import (
    PromptConfig, 
    FIIN_VERTICAL_PROMPT_UNIVERSAL_OPENAI_EXTEND
)
from initialize import initialize_text2sql
from ETL.dbmanager import get_semantic_layer, BaseRerannk

import api.configuration as config

def initialize(chat_model, text2sql_model):
    if chat_model is not None:
        return initialize_chat_bot(chat_model=chat_model, text2sql_model=text2sql_model)
    return initialize_text2sql_model(text2sql_model=text2sql_model)
    
def initialize_chat_bot(chat_model = 'gemini-2.0-flash', text2sql_model = 'gemini-2.0-flash'):
    prompt_config = FIIN_VERTICAL_PROMPT_UNIVERSAL_OPENAI_EXTEND
    text2sql_config = TEXT2SQL_FAST_GEMINI_CONFIG
    chat_config = GEMINI_FAST_CONFIG_V2

    if 'gemini-2.0-flash' in chat_model:
        chat_config = GEMINI_FAST_CONFIG
    if 'gpt-4o-mini' in chat_model:
        chat_config = GPT4O_MINI_CONFIG
    elif 'gpt-4o' in chat_model:
        chat_config = GPT4O_CONFIG

    if 'qwen2.5-3b-sft' in text2sql_model:
        text2sql_config = TEXT2SQL_QWEN25_CODER_3B_SFT_CONFIG
    elif 'qwen2.5-1.5b-kto' in text2sql_model:
        text2sql_config = TEXT2SQL_QWEN25_CODER_1B_KTO_CONFIG
    elif 'gpt-4o-mini' in text2sql_model:
        text2sql_config = TEXT2SQL_FAST_OPENAI_CONFIG
    elif 'gpt-4o' in text2sql_model:
        text2sql_config = TEXT2SQL_4O_CONFIG
    elif 'gemini-2.0-flash-thinking-exp-01-21' in text2sql_model:
        text2sql_config = TEXT2SQL_THINKING_GEMINI_CONFIG
    
    text2sql = initialize_text2sql(text2sql_config, prompt_config, version = config.VERSION, rotate_key = config.ROTATE_API)
    
    message_saver = get_semantic_layer()
    
    chatbot = ChatbotSematic(config = ChatConfig(**chat_config), text2sql = text2sql, message_saver = message_saver)
    
    chatbot.create_new_chat(user_id='admin')
    
    return chatbot    

def initialize_text2sql_model(text2sql_model = 'gemini-2.0-flash'):
    prompt_config = FIIN_VERTICAL_PROMPT_UNIVERSAL_OPENAI_EXTEND
    text2sql_config = TEXT2SQL_FAST_GEMINI_CONFIG

    if 'qwen2.5-3b-sft' in text2sql_model:
        text2sql_config = TEXT2SQL_QWEN25_CODER_3B_SFT_CONFIG
    elif 'qwen2.5-3b-kto' in text2sql_model:
        text2sql_config = TEXT2SQL_QWEN25_CODER_3B_KTO_CONFIG
    elif 'gpt-4o-mini' in text2sql_model:
        text2sql_config = TEXT2SQL_FAST_OPENAI_CONFIG
    elif 'gpt-4o' in text2sql_model:
        text2sql_config = TEXT2SQL_4O_CONFIG
    elif 'gemini-2.0-flash-thinking-exp-01-21' in text2sql_model:
        text2sql_config = TEXT2SQL_THINKING_GEMINI_CONFIG
    elif 'gemini-2.0-pro-exp' in text2sql_model:
        text2sql_config = TEXT2SQL_GEMINI_PRO_EXP_CONFIG
    
    chatbot = initialize_text2sql(text2sql_config, prompt_config, version = config.VERSION, message=True, rotate_key = config.ROTATE_API)

    return chatbot