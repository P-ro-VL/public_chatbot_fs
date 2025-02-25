# Chatbot_financial_statement (public)

## File structures

### Agent

This is the codebase for Text2SQL Agent and Chatbot

- Agent: Text2SQL solver, Text2SQL configs
- Chatbot: Normal Chatbot, Chatbot with Semantic Layers.
- Prompts

### ETL

This is the codebase for database setup and DB utils for Text2SQL solver and Chatbot (access to Postgre and vectordb) 

- DBManager: Connect to RDB and doing vector search and rerank. Also include Semantic Layers
- Connector: Utils and setup for RDB and vectordb
- Ratio_index, const, etl: Create financial ratio, merge financial statements

### Page

- Host the Chatbot via steamlit

### Trainer

- GPRO Trainer

## LLM Available

### Gemini:

- Gemini 2.0 Flash
- Gemini 2.0 Flash Thinking Exp

### GPT

- GPT 4o mini (Local test: 0.65)
- GPT 4o

### Deepseek

- Deepseek-chat

## Database design

- Horizontal: Each account/ratio is a columns in the main table
- Vertical: Each account/ratio is a row in the main table

## Prompting Strategy
- General: 2-step Text2sql. First asking LLM to analyze the problem and choose which category do they want to access. Then adding snapshot of the table into prompt, so it can correctly select the right column.
- Reasoning: After having snapshot, ask LLM to generate SQL directly to solve the problem
- Include debugging

## Setup guide
<details>
<summary>Ignore</summary>
- Make `run.sh` file executable
```bash
chmod +x run.sh
```

- For CPU (Using OpenAI Embedding)
```bash
./run.sh --openai True
```

- For GPU (Self-hosted Embedding Server)
```bash
./run.sh local-embedding --local True
```
- For GPU, Including Reranker 
```bash
./run.sh local-server --local True 
```
</details>

### Setup maunally



Clone the reporitoty and create environment

```bash
git clone https://github.com/hung20gg/public_chatbot_fs.git
cd public_chatbot_fs
git clone https://github.com/hung20gg/llm.git

conda create -y -n text2sql
conda activate text2sql
pip install -r requirements.txt
```

**Prepare env file**
Create a `.env` file and put all the necessary key into it
```
OPENAI_API_KEY=your_api_key
GEMINI_API_KEY=your_api_key

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

MONGO_DB_HOST=
MONGO_DB_USER=
MONGO_DB_PASSWORD=
MONGO_DB_PORT=

EMBEDDING_SERVER_URL=http://localhost:8080
EMBEDDING_MODEL=BAAI/bge-base-en-v1.5

RERANKER_SERVER_URL=http://localhost:8081
RERANKER_MODEL=BAAI/bge-reranker-v2-m3

LOCAL_EMBEDDING=True


DEEPSEEK_HOST=https://api.deepseek.com
DEEPSEEK_API_KEY=your_api_key

LLM_HOST=http://localhost:8000/v1
```
Then run
```
# Linux, macos
source .env

# Window
.env
```

#### Local Embedding
**Note** Build the TEI local and run the following scripts (check the [TEI repo](https://github.com/huggingface/text-embeddings-inference) for setup)

- For embedding:
```bash
model=BAAI/bge-base-en-v1.5
text-embeddings-router --model-id $model --port 8080
```

- For Reranker (it is ok not to have reranker)
```bash
model=BAAI/bge-reranker-v2-m3
text-embeddings-router --model-id $model --port 8081
```

#### Setup database
Using any existing database or using Docker Image for:
- Postgre
- MongoDB (optional)

Create database via this scripts (notice the version)

```bash
python setup.py --preprocess v3 --force True --local True --vectordb chromadb
```

For using data of 200 companies
```bash
python setup.py --preprocess v3.2 --force True --local True --vectordb chromadb
```

**Note:** If you are not using local embedding, remove `--local True` and replace with `--openai True`

Run the `test.py` file to check the setup status
```bash
python test.py
```

### DB In the pipeline
- ChromaDB/ Milvus (Storing the embedding)
- PostgreSQL (Storing the data)
- MongoDB (Storing the user message)



Check and add the index for full-text search in [ETL\index_full_text_search.md](ETL\index_full_text_search.md)
