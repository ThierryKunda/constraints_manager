from fastapi import FastAPI
import data_models

app = FastAPI()


@app.get("/generate_planning")
async def generate_planning():
    return {
        "confirmation_status": "generating"
    }

@app.get("/get_planning")
async def get_planning() -> list[data_models.Slot] | dict:
    pass