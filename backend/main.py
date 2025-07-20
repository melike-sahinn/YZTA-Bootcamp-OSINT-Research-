# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Proje içi modül importları
# Maps yerine osm_geocoding kullanıyoruz
from .api import afad, osm_geocoding, llm_assist  # llm_assist de artık statik yanıtlar veriyor
from .models.data_models import ResearchQuery, InfoRequest

app = FastAPI(
    title="OSINT for Daily Life API",
    description="Açık kaynak istihbaratı ile günlük yaşam sorunlarına çözümler sunan API.",
    version="0.1.0"
)

# CORS ayarları
origins = [
    "http://localhost",
    "http://localhost:8501",  # Streamlit'in varsayılan portu
    "http://127.0.0.1:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "OSINT for Daily Life API'ye hoş geldiniz!"}


# --- Mod 1: Kendi Araştırmanı Yap Akışı ---
@app.post("/research/suggest_sources")
async def suggest_research_sources(query: ResearchQuery):
    """
    Kullanıcının araştırma konusuna göre kaynak önerileri sunar (AI kullanılmıyor).
    """
    try:
        sources = await llm_assist.get_research_suggestions(query.topic, query.keywords)
        return {"topic": query.topic, "suggestions": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kaynak önerileri alınırken hata oluştu: {e}")


# --- Mod 2: Hazır Bilgi Akışı ---
@app.post("/info/get_summary")
async def get_predefined_info_summary(request: InfoRequest):
    """
    Belirli bir konu hakkında web scraping ve basit özetleme ile hazır bilgi sunar (AI kullanılmıyor).
    """
    try:
        summary_text = ""
        if request.topic == "afad_toplanma_alanlari":
            data = await afad.get_afad_collection_areas(request.location)
            if "error" in data:
                summary_text = data["error"]
            else:
                # AFAD verisini doğrudan özetle fonksiyonuna gönderiyoruz
                summary_text = await llm_assist.summarize_data(data, "AFAD Toplanma Alanları")
        else:
            # Genel web scraping ve basit özetleme
            scraped_content = await llm_assist.perform_web_scraping(request.topic)
            summary_text = await llm_assist.summarize_data(scraped_content, request.topic)

        return {"topic": request.topic, "summary": summary_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hazır bilgi alınırken hata oluştu: {e}")


# --- Harita Entegrasyonu ---
@app.get("/map/search_location")
async def search_location_on_map(query: str):
    """
    OpenStreetMap Nominatim API kullanarak bir konumu haritada arar ve koordinatlarını döndürür.
    """
    try:
        location_data = await osm_geocoding.search_location(query)  # Maps yerine osm_geocoding
        if "error" in location_data:
            raise HTTPException(status_code=400, detail=location_data["error"])
        return location_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Harita araması başarısız oldu: {e}")


# --- Chatbot Akışı ---
@app.post("/chatbot/chat")
async def chat_with_bot(request: dict):
    """
    OSINT chatbot ile sohbet eder (AI kullanılmıyor, basit kural tabanlı yanıtlar).
    """
    user_message = request.get("user_message")
    chat_history = request.get("chat_history", [])

    if not user_message:
        raise HTTPException(status_code=400, detail="Kullanıcı mesajı boş olamaz.")

    try:
        bot_response = await llm_assist.chat_with_osint_bot(user_message, chat_history)
        return {"response": bot_response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot yanıtı alınırken hata oluştu: {e}")


# --- Uygulamayı Çalıştırma ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)