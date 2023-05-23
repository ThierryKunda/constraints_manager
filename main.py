from fastapi import FastAPI
import data_models
import uvicorn

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

@app.get("/get_planning")
async def get_planning() -> list[data_models.Slot] | dict:
    pass

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    