import requests
from bs4 import BeautifulSoup
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio # Bu satır eklendi!

# .env dosyasını yükle
load_dotenv()

# Gemini API anahtarını al
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Anahtarın gerçekten yüklendiğini kontrol et
if not GEMINI_API_KEY:
    print("HATA: GEMINI_API_KEY .env dosyasında tanımlı değil veya boş!")
    raise ValueError("GEMINI_API_KEY, .env dosyasında tanımlı değil veya boş!")

# Gemini modeli için yapılandırma
try:
    genai.configure(api_key=GEMINI_API_KEY)
    # Model ismini 'gemini-1.5-flash' olarak kullanıyoruz
    test_model = genai.GenerativeModel('gemini-1.5-flash')

    # Modelin erişilebilirliğini test etmek için küçük bir deneme yapıyoruz.
    test_response = test_model.generate_content(
        "Merhaba, test için basit bir yanıt ver."
    )

    if test_response and test_response.text:
        model = test_model
        print("INFO: Gemini API başarıyla yapılandırıldı ve test edildi.")
    else:
        print(f"UYARI: İlk Gemini test yanıtı boş geldi veya .text alanı yok. Ham yanıt: {test_response}")
        raise Exception("Gemini API ilk test yanıtı alınamadı veya boş geldi.")
except Exception as e:
    print(f"KRİTİK HATA: Gemini API yapılandırma veya ilk test sırasında hata oluştu: {e}")
    print("Lütfen API anahtarınızın doğru, aktif ve internet bağlantınızın olduğundan emin olun.")
    model = None


# --- Ortak Yardımcı Fonksiyon ---
async def generate_gemini_response(prompt: str, history: list = None):
    """
    Google Gemini modelinden yanıt alır.
    Eğer Gemini modeli kullanılamıyorsa, bir hata mesajı döndürür.
    """
    if model is None:
        print("DEBUG: generate_gemini_response çağrıldı ama model None. Varsayılan yanıt dönüyor.")
        return "Üzgünüm, yapay zeka modeli şu anda kullanılamıyor. Lütfen API anahtarınızı kontrol edin."

    response = None # response değişkenini None olarak başlatıyoruz
    try:
        gemini_history = []
        if history:
            for msg in history:
                # Sohbet geçmişindeki mesajların geçerliliğini daha sıkı kontrol ediyoruz.
                # 'msg' bir sözlük mü, 'role' ve 'content' anahtarları var mı ve boş değiller mi?
                if msg and isinstance(msg, dict) and msg.get("role") and msg.get("content"):
                    if msg["role"] == "user":
                        # İçeriği her ihtimale karşı string'e çeviriyoruz
                        gemini_history.append({"role": "user", "parts": [str(msg["content"])]})
                    elif msg["role"] == "assistant":
                        # 'assistant' rolünü Gemini'nin beklediği 'model'e çeviriyoruz ve içeriği string'e çeviriyoruz
                        gemini_history.append({"role": "model", "parts": [str(msg["content"])]})
                else:
                    print(f"UYARI: Geçersiz veya eksik sohbet geçmişi mesajı atlandı: {msg}")


        convo = model.start_chat(history=gemini_history)

        print(f"DEBUG: Gemini'ye gönderilen prompt: '{prompt}'")

        # Gemini API çağrısını ayrı bir try-except bloğuna alıyoruz
        # Bu, bağlantı sorunları veya API'nin yanıt vermemesi gibi durumları yakalar.
        try:
            response = await convo.send_message_async(prompt)
            # --- ORAN SINIRLAMASI TESTİ İÇİN GEÇİCİ OLARAK EKLE ---
            # Eğer ilk mesaj sonrası sorun yaşıyorsan, buradaki yorumu kaldırıp deneme yapabilirsin.
            # await asyncio.sleep(1) # Her yanıttan sonra 1 saniye bekler. Test sonrası kaldırılabilir/azaltılabilir.
            # --- TEST BİTTİ ---

        except Exception as api_call_e:
            print(f"KRİTİK API ÇAĞRISI HATASI: send_message_async sırasında hata oluştu: {api_call_e}")
            return f"Üzgünüm, yapay zeka modeline mesaj gönderilirken bir hata oluştu: '{api_call_e}'. Lütfen daha sonra tekrar deneyin."

        # Eğer API'den None bir yanıt gelirse (API'nin kendisi bir hata fırlatmadan boş döndürürse)
        if response is None:
            print("UYARI: send_message_async'ten yanıt nesnesi gelmedi (None).")
            return "Üzgünüm, yapay zekadan beklenmedik bir yanıt alındı veya bağlantı sorunu oluştu. Lütfen tekrar deneyin."

        print(f"DEBUG: Gemini'den gelen HAM YANIT NESNESİ: {response}")

        # Güvenlik ayarları kontrolü: Eğer yanıt güvenlik politikaları nedeniyle engellendiyse
        if hasattr(response, 'prompt_feedback') and response.prompt_feedback and response.prompt_feedback.block_reason:
            reason = response.prompt_feedback.block_reason
            print(f"UYARI: Gemini yanıtı güvenlik nedeniyle engelledi. Neden: {reason}")
            return f"Üzgünüm, bu soru güvenlik politikaları nedeniyle yanıtlanamadı. Neden: {reason}"

        # Aday yanıtları ve içeriği kontrol etmeden önce 'candidates' özelliğinin varlığını kontrol et
        if hasattr(response, 'candidates') and response.candidates:
            for candidate in response.candidates:
                # Adayın içeriği ve parçaları var mı kontrol et
                if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                    # Yanıt parçalarını birleştiriyoruz ve 'text' özelliğinin varlığını kontrol ediyoruz
                    response_text = "".join([part.text for part in candidate.content.parts if hasattr(part, 'text')])
                    if response_text:
                        print(f"DEBUG: Gemini'den başarılı yanıt metni: '{response_text}'")
                        return response_text

        # Hiçbir geçerli yanıt alınamadıysa veya yukarıdaki kontrollerden geçmediyse
        print(f"UYARI: Gemini'den beklenen yanıt metni gelmedi veya boştu. Ham yanıt detayları: {response}")
        return "Üzgünüm, yapay zekadan net bir yanıt alınamadı veya bir sorun oluştu. Lütfen farklı bir soru deneyin."

    except Exception as e:
        # Yakalanan her genel hata için detaylı loglama ve kullanıcıya bilgi
        error_details = f"Ham hata nesnesi veya detayları: {response if response is not None else 'Yanıt nesnesi yok'}"
        print(f"KRİTİK API YANIT HATASI: {e}. {error_details}")
        return f"Üzgünüm, yapay zeka yanıtı alınırken bir sorun oluştu: '{e}'. Lütfen daha sonra tekrar deneyin veya API anahtarınızı kontrol edin."


# --- Mod 1: Kendi Araştırmanı Yap Akışı ---
async def get_research_suggestions(topic: str, keywords: list[str]):
    """
    Konu ve anahtar kelimelere göre araştırma kaynakları önerir (Gemini destekli).
    """
    if model is None:
        return "Üzgünüm, yapay zeka modeli kullanılamadığından araştırma önerileri veremiyorum."

    prompt = f"OSINT (Açık Kaynak İstihbaratı) prensiplerini kullanarak '{topic}' konusu ve anahtar kelimeler '{', '.join(keywords)}' hakkında güvenilir ve ulaşılabilir araştırma kaynakları önerileri listeler misin? Kaynakları türlerine göre (örn: resmi siteler, akademik veritabanları, raporlar, haber kaynakları vb.) ayırabilirsin. Yanıtını maddeler halinde ve açıklayıcı bir şekilde ver."
    response = await generate_gemini_response(prompt, history=[])  # Yeni bir sohbet başlat
    return response


async def perform_web_scraping(query: str):
    """
    Basit bir web scraping işlemi yapar.
    Not: Büyük siteler bot engellemeleri yapabilir, bu kısım her zaman stabil olmayabilir.
    """
    try:
        search_url = f"https://www.google.com/search?q={query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for g in soup.find_all('div', class_='g'):
            link_tag = g.find('a')
            title_tag = g.find('h3')
            if link_tag and title_tag:
                title = title_tag.get_text()
                link = link_tag.get('href')
                if link and (link.startswith("http://") or link.startswith("https://")):
                    results.append(f"Başlık: {title}\nLink: {link}\n")

        return "\n".join(results[
                         :5]) if results else "Web'den veri çekilemedi veya sonuç bulunamadı. (Bot engellemesi veya yapısal değişiklik olabilir.)"
    except requests.exceptions.RequestException as e:
        return f"Web scraping hatası (bağlantı/HTTP): {e}. Belki de belirli bir URL hedeflemelisiniz veya VPN denemelisiniz."
    except Exception as e:
        return f"Web scraping beklenmedik hata: {e}."


async def summarize_data(data: dict or str or list, topic: str):
    """
    Verilen veriyi Gemini kullanarak özetler.
    """
    if model is None:
        return "Üzgünüm, yapay zeka modeli kullanılamadığından veri özetlenemiyor."

    # Veriyi Gemini'nin işleyebileceği bir string formatına çevir
    if isinstance(data, (dict, list)):
        data_str = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        data_str = str(data)

    # Context penceresi limitini aşmamak için kontrol
    if len(data_str) > 25000: # Gemini Pro'nun genel limitleri için biraz pay bırakalım
        data_str = data_str[:24000] + "\n...[Veri kırpıldı, çok uzun olduğu için.]"

    prompt = f"Aşağıdaki veriyi '{topic}' konusu özelinde özetler misin? Özellikle önemli bilgileri ve ana noktaları vurgula. Yanıtını anlaşılır ve öz bir şekilde paragraflar halinde düzenle.\n\nVeri:\n{data_str}"

    response = await generate_gemini_response(prompt, history=[]) # Yeni bir sohbet başlat
    return response


async def chat_with_osint_bot(user_message: str, chat_history: list[dict]):
    """
    Kullanıcı mesajına göre OSINT botu ile sohbet eder (Gemini destekli).
    """
    if model is None:
        return "Üzgünüm, yapay zeka modeli şu anda kullanılamıyor. Lütfen API anahtarınızı kontrol edin."

    gemini_history = []
    for msg in chat_history:
        # Geçmişteki mesajların sağlamlığını kontrol ediyoruz
        if msg and isinstance(msg, dict) and msg.get("role") and msg.get("content"):
            if msg["role"] == "user":
                gemini_history.append({"role": "user", "parts": [str(msg["content"])]}) # Content'i stringe çevir
            elif msg["role"] == "assistant":
                # 'assistant' rolünü Gemini'nin beklediği 'model'e çeviriyoruz ve içeriği string'e çeviriyoruz
                gemini_history.append({"role": "model", "parts": [str(msg["content"])]})
        else:
            print(f"UYARI: chat_with_osint_bot içinde geçersiz sohbet geçmişi mesajı atlandı: {msg}")

    prompt = user_message

    response = await generate_gemini_response(prompt, gemini_history)
    return response