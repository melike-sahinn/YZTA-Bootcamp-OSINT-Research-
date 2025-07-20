# backend/api/afad.py
import requests
import json


async def get_afad_collection_areas(location: str):
    """
    Belirtilen konum için AFAD toplanma alanlarını çeker.
    Bu kısım gerçek bir AFAD API'si ile entegre edilmelidir.
    Şimdilik örnek (mock) veri döndürecektir.
    """
    # Gerçek bir API entegrasyonunda:
    # try:
    #     response = requests.get(f"https://api.afad.gov.tr/toplanma-alanlari?konum={location}")
    #     response.raise_for_status()
    #     return response.json()
    # except Exception as e:
    #     print(f"AFAD verisi çekilirken hata: {e}")
    #     return {"error": "AFAD verisi alınamadı."}

    # Örnek (Mock) Veri
    mock_data = {
        "Ankara/Çankaya": [
            {"name": "Kuğulu Park", "latitude": 39.9079, "longitude": 32.8540,
             "address": "Kavaklıdere, Çankaya/Ankara"},
            {"name": "Anıtpark", "latitude": 39.9169, "longitude": 32.8447, "address": "Mebusevleri, Çankaya/Ankara"},
        ],
        "Istanbul/Kadıköy": [
            {"name": "Yoğurtçu Parkı", "latitude": 40.9859, "longitude": 29.0270,
             "address": "Osmanağa, Kadıköy/İstanbul"},
            {"name": "Özgürlük Parkı", "latitude": 40.9800, "longitude": 29.0600,
             "address": "Göztepe, Kadıköy/İstanbul"}
        ]
    }

    # Lokasyona göre basit bir eşleşme yapıyoruz
    for key, value in mock_data.items():
        if location.lower() in key.lower():
            return value

    return {"error": "Belirtilen konum için AFAD verisi bulunamadı veya örnek veride mevcut değil."}