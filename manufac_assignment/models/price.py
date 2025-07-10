from pydantic import BaseModel

class PricePoint(BaseModel):
    date: str
    price: float
    unit: str

class MovingAveragePoint(BaseModel):
    date: str
    price: float
    ma: float

class AnomalyPoint(BaseModel):
    date: str
    price: float
    z: float
    isAnomaly: bool