from fastapi import FastAPI
import data_models
import uvicorn
import json

app = FastAPI()

@app.get("/")
async def gen():
    return{
        "message" : "hello world"
    }

@app.get("/generate_planning")
async def generate_planning():
    return {
        "confirmation_status": "generating"
    }

@app.get("/get_planning/{annee}")
async def get_planning(annee: int) -> dict:
    content = {}
    with open(f"./plannings/{annee}.json", 'r') as f:
        content = f.read()
    return json.loads(content)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    