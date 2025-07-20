# backend/api/osm_geocoding.py
import requests

async def search_location(query: str):
    """
    OpenStreetMap Nominatim API kullanarak bir konumun koordinatlarını arar.
    Tamamen ücretsizdir.
    """
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "OSINTforDailyLifeApp/1.0 (contact@example.com)" # Uygulama adın ve iletişim bilgin
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status() # HTTP hatalarını kontrol et
        data = response.json()

        if data:
            location = data[0]
            return {
                "latitude": float(location["lat"]),
                "longitude": float(location["lon"]),
                "formatted_address": location["display_name"]
            }
        else:
            return {"error": "Konum bulunamadı. Lütfen daha spesifik bir arama yapın."}
    except requests.exceptions.RequestException as e:
        return {"error": f"OpenStreetMap API'ye bağlanırken hata oluştu: {e}"}
    except Exception as e:
        return {"error": f"Bir hata oluştu: {e}"}