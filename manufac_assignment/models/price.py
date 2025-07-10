from pydantic import BaseModel

class PricePoint(BaseModel):
    date: str
    price: float
    unit: str

class MovingAveragePoint(PricePoint):
    ma: float

class AnomalyPoint(PricePoint):
    z: float
    isAnomaly: bool 