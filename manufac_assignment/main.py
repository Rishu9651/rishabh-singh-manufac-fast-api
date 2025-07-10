from fastapi import FastAPI
from manufac_assignment.api.v1 import router as v1_router

app = FastAPI(title="India Metro Fuel-Price Time-Series API")

app.include_router(v1_router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "India Metro Fuel-Price Time-Series API is running."} 