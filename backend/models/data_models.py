# backend/models/data_models.py
from pydantic import BaseModel
from typing import List, Optional

class ResearchQuery(BaseModel):
    """
    Araştırma sorguları için veri modeli.
    """
    topic: str
    keywords: Optional[List[str]] = None

class InfoRequest(BaseModel):
    """
    Hazır bilgi talepleri için veri modeli.
    """
    topic: str
    location: Optional[str] = None

# AFAD verisi için örnek bir model (gerçekte AFAD API yanıtına göre düzenlenmeli)
class AfadCollectionArea(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    # AFAD'dan gelen diğer alanlar buraya eklenebilir