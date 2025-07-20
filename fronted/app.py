import streamlit as st
import requests
import json
import time

# Sayfa yapılandırması
st.set_page_config(layout="wide", page_title="OSINT for Daily Life", page_icon="🕵️")

# Eğer yoksa, session_state'i başlat
if "messages" not in st.session_state:
    st.session_state.messages = []
# Giriş kaldırıldığı için artık authenticated durumuna gerek yok.
# Ama yine de tutalım, belki gelecekte eklemek istersin. Varsayılan olarak True yapalım.
if "authenticated" not in st.session_state:
    st.session_state.authenticated = True  # Herkese açık olduğu için varsayılan True
if "username" not in st.session_state:
    st.session_state.username = "Guest"  # Kullanıcı adı varsayılan olarak "Guest"
if "page_selection" not in st.session_state:
    st.session_state.page_selection = "Ana Sayfa"  # Başlangıçta Ana Sayfa seçili gelsin

# Backend API URL'i
BASE_API_URL = "http://localhost:8000"

# --- Sidebar (Yan Panel) ---
with st.sidebar:
    st.markdown("---")  # Üstte bir çizgi ekleyelim
    st.title("🕵️‍♂️ OSINT for Daily Life")  # Daha büyük başlık ve ikon
    st.write("### Günlük Yaşam Sorunlarına Açık Veriyle Çözüm")  # Daha belirgin bir slogan
    st.markdown("---")  # Bir çizgi daha

    st.write("#### Nasıl ilerlemek istersiniz?")

    # Navigasyon Butonları (Daha Şık Bir Görünüm İçin)
    # Her butona bir anahtar (key) ve bir callback fonksiyonu atayarak sayfa geçişini yönetiyoruz.
    if st.button("🏡 Ana Sayfa", key="nav_home", use_container_width=True):
        st.session_state.page_selection = "Ana Sayfa"
    if st.button("🔬 Kendi Araştırmamı Yap", key="nav_research", use_container_width=True):
        st.session_state.page_selection = "Kendi Araştırmamı Yap"
    if st.button("📚 Hazır Bilgi AI", key="nav_ready_info", use_container_width=True):
        st.session_state.page_selection = "Hazır Bilgi AI"
    if st.button("💬 Chatbot ile Sohbet Et", key="nav_chatbot", use_container_width=True):
        st.session_state.page_selection = "Chatbot ile Sohbet Et"
    if st.button("🔍 Sorun Tespit Et", key="nav_detect_problem", use_container_width=True):
        st.session_state.page_selection = "Sorun Tespit Et"
    if st.button("🤝 Ortak Fayda Ara", key="nav_find_common_benefit", use_container_width=True):
        st.session_state.page_selection = "Ortak Fayda Ara"

    st.markdown("---")  # Ayırıcı çizgi

    # Proje Vizyonu (Expander içinde daha düzenli)
    with st.expander("Proje Vizyonu", expanded=False):  # Başlangıçta kapalı olsun
        st.info(
            """
            Proje Vizyonu: Bireylerin gündelik yaşamlarında karşılaştıkları sorunlara 
            açık veri ile çözüm aramalarını kolaylaştıran, etik ilkelerle yönlendiren, 
            yapay zekâ destekli bir dijital rehberdir.
            """
        )

    st.markdown("---")  # Ayırıcı çizgi

    # Giriş kaldırıldığı için kullanıcı bilgisini sadeleştiriyoruz
    st.success(f"Hoş Geldin, {st.session_state.username}!")


# --- Ana İçerik Alanı ---
# Artık giriş kontrolüne gerek yok, doğrudan içeriği gösteriyoruz.
if st.session_state.page_selection == "Ana Sayfa":
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🏡 OSINT for Daily Life'a Hoş Geldiniz!</h1>",
                unsafe_allow_html=True)
    st.markdown("---")

    st.write("""
        Merhaba! Günlük hayatınızda karşılaştığınız sorunlara açık kaynak istihbaratı (OSINT) 
        teknikleriyle çözüm bulmanıza yardımcı olacak dijital rehberinize hoş geldiniz. 
        Amacımız, bilgiye erişimi kolaylaştırmak ve doğru kararlar almanıza destek olmaktır.
    """)
    st.markdown("---")

    # Kartlar veya Sütunlar ile Özellikleri Vurgulama
    st.subheader("💡 Projenin Temel Özellikleri:")
    col1, col2, col3 = st.columns(3)  # 3 sütun oluştur

    with col1:
        st.info("### Kendi Araştırmamı Yap")
        st.write(
            "Belirli bir konu hakkında derinlemesine OSINT araştırması yapın. Güvenilir kaynakları keşfedin ve bilgi toplayın.")
        st.write("🔎 Detaylı bilgi toplama")
        st.write("📊 Veri analizi ve raporlama")

    with col2:
        st.info("### Chatbot ile Sohbet Et")
        st.write(
            "Yapay zeka destekli sohbet botumuzla anlık olarak etkileşime geçin. Sorular sorun ve anında yanıtlar alın.")
        st.write("💬 Hızlı yanıtlar")
        st.write("🧠 Akıllı rehberlik")

    with col3:
        st.info("### Sorun Tespit Et & Çözüm Bul")
        st.write(
            "Günlük yaşamdaki problemleri tanımlayın, olası nedenleri araştırın ve açık verilerle potansiyel çözümler keşfedin.")
        st.write("🎯 Problem analizi")
        st.write("🛠️ Çözüm önerileri")

    st.markdown("---")
    st.subheader("✨ OSINT'in Gücü")
    st.write("""
        Açık kaynak istihbaratı (OSINT), halka açık kaynaklardan bilgi toplama ve analiz etme sürecidir. 
        Bu proje ile OSINT'in gücünü kullanarak aşağıdaki gibi birçok konuda size yardımcı olabiliriz:
        * **Güvenlik:** Dolandırıcılık tespiti, sahte ürün analizi.
        * **Tüketici Hakları:** Ürün/hizmet şikayetleri, şirket itibarı araştırması.
        * **Gayrimenkul:** Bir bölge hakkında bilgi toplama, geçmiş verileri inceleme.
        * **Seyahat:** Güvenli seyahat planlaması, yerel bilgiler edinme.
        * **Eğitim:** Okul/kurum araştırması, akademik kaynak bulma.

        Unutmayın, tüm araştırmalar etik sınırlar içinde ve yasalara uygun olarak yapılmalıdır.
    """)

elif st.session_state.page_selection == "Kendi Araştırmamı Yap":
    st.header("🔬 Kendi Araştırmanı Yap")
    st.write("Lütfen araştırmak istediğiniz konuyu ve anahtar kelimeleri girin.")

    research_topic = st.text_input("Araştırma Konusu:", key="research_topic_input")
    keywords_input = st.text_input("Anahtar Kelimeler (virgülle ayırın):", key="keywords_input")

    if st.button("Araştırma Önerileri Al", key="get_suggestions_button"):
        if research_topic and keywords_input:
            keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
            with st.spinner("Araştırma önerileri hazırlanıyor..."):
                try:
                    response = requests.post(f"{BASE_API_URL}/research_suggestions",
                                             json={"topic": research_topic, "keywords": keywords})
                    if response.status_code == 200:
                        st.subheader("Araştırma Önerileri:")
                        st.markdown(response.json().get("suggestions", "Öneri alınamadı."))
                    else:
                        st.error(f"API Hatası: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Backend sunucusuna bağlanılamadı. Lütfen backend'in çalıştığından emin olun.")
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("Lütfen araştırma konusu ve anahtar kelimeleri girin.")

    st.markdown("---")
    st.subheader("Web'den Veri Çek")
    web_query = st.text_input("Web'den Çekilecek Bilgi/Anahtar Kelime:", key="web_query_input")
    if st.button("Veri Çek", key="scrape_data_button"):
        if web_query:
            with st.spinner("Web'den veri çekiliyor..."):
                try:
                    response = requests.post(f"{BASE_API_URL}/web_scrape", json={"query": web_query})
                    if response.status_code == 200:
                        scraped_data = response.json().get("data", "Veri çekilemedi.")
                        st.text_area("Çekilen Veriler:", scraped_data, height=300, key="scraped_data_output")
                    else:
                        st.error(f"API Hatası: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Backend sunucusuna bağlanılamadı. Lütfen backend'in çalıştığından emin olun.")
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("Lütfen web'den çekilecek bir sorgu girin.")

    st.markdown("---")
    st.subheader("Veri Özeti Oluştur")
    summary_data = st.text_area("Özetlenecek Veri:", height=200, key="summary_data_input")
    summary_topic = st.text_input("Özet Konusu:", key="summary_topic_input")
    if st.button("Veriyi Özetle", key="summarize_button"):
        if summary_data and summary_topic:
            with st.spinner("Veri özetleniyor..."):
                try:
                    response = requests.post(f"{BASE_API_URL}/summarize_data",
                                             json={"data": summary_data, "topic": summary_topic})
                    if response.status_code == 200:
                        st.subheader("Özet:")
                        st.markdown(response.json().get("summary", "Özet oluşturulamadı."))
                    else:
                        st.error(f"API Hatası: {response.status_code} - {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("Backend sunucusuna bağlanılamadı. Lütfen backend'in çalıştığından emin olun.")
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
        else:
            st.warning("Lütfen özetlenecek veri ve özet konusu girin.")


elif st.session_state.page_selection == "Hazır Bilgi AI":
    st.header("📚 Hazır Bilgi AI")
    st.info(
        "Bu bölüm, sıkça sorulan OSINT konuları hakkında önceden hazırlanmış, yapay zeka tarafından derlenmiş bilgilere hızlıca ulaşmanızı sağlayacaktır.")
    st.write("Geliştirme aşamasındadır.")


elif st.session_state.page_selection == "Chatbot ile Sohbet Et":
    st.header("🤖 Chatbot ile Sohbet Et")
    st.write("Yapay zeka destekli OSINT botunuzla sohbet edin. Merak ettiklerinizi sorun!")

    # Sohbet geçmişini göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcıdan girdi al
    if prompt := st.chat_input("Mesajınızı buraya yazın...", key="chatbot_input"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Yapay zeka düşünüyor..."):
                try:
                    # Backend'e mesaj ve geçmişi gönder
                    # Dikkat: sohbet geçmişini API'ye uygun formatta gönderiyoruz
                    response = requests.post(f"{BASE_API_URL}/chatbot/chat",
                                             json={"user_message": prompt, "chat_history": st.session_state.messages})

                    if response.status_code == 200:
                        full_response = response.json().get("response", "Üzgünüm, yanıt alınamadı.")
                        st.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                    else:
                        st.error(f"API Hatası: {response.status_code} - {response.text}")
                        st.session_state.messages.append(
                            {"role": "assistant", "content": f"Hata: {response.status_code} - {response.text}"})
                except requests.exceptions.ConnectionError:
                    st.error("Backend sunucusuna bağlanılamadı. Lütfen backend'in çalıştığından emin olun.")
                    st.session_state.messages.append(
                        {"role": "assistant", "content": "Hata: Backend sunucusuna bağlanılamadı."})
                except Exception as e:
                    st.error(f"Bir hata oluştu: {e}")
                    st.session_state.messages.append({"role": "assistant", "content": f"Beklenmedik hata: {e}"})

elif st.session_state.page_selection == "Sorun Tespit Et":
    st.header("🔍 Sorun Tespit Et")
    st.info(
        "Bu bölüm, günlük yaşamınızdaki belirli sorunları daha derinlemesine analiz etmenize ve olası nedenleri açık kaynaklarla araştırmanıza yardımcı olacaktır.")
    st.write("Geliştirme aşamasındadır.")

elif st.session_state.page_selection == "Ortak Fayda Ara":
    st.header("🤝 Ortak Fayda Ara")
    st.info(
        "Bu bölüm, benzer sorunlar yaşayan veya benzer hedefleri olan kişi ve toplulukları açık kaynak verileriyle bulmanıza yardımcı olacaktır.")
    st.write("Geliştirme aşamasındadır.")
