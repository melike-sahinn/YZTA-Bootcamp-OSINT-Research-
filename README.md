# YZTA-Bootcamp-OSINT-Research-
Proje Vizyonu

"OSINT for Daily Life", bireylerin gündelik yaşamlarında karşılaştıkları sorunlara açık veri ile çözüm aramalarını kolaylaştıran, etik ilkelerle yönlendiren, yapay zekâ destekli bir dijital rehberdir.

Projede kullanıcılar:

Ya kendi araştırmasını yapmayı öğrenir,

Ya da AI destekli asistanın topladığı hazır veriye ulaşır.


Bu sayede:

Araştırma ve sorgulama becerileri gelişir,

Yerel sorunları fark eder,

Belediyelerle daha bilinçli ve yapıcı iletişim kurabilirler.



---

 1. Sprint Kapsamı

 Hedeflenen Çıktılar:

Proje fikrinin netleştirilmesi

Rol dağılımının yapılması

Projenin eğitim temasıyla ilişkilendirilerek gerekçelendirilmesi

Kullanıcı modlarının (Mod 1 ve Mod 2) belirlenmesi

Kullanıcı profillerinin tanımlanması

Teknoloji stack’inin belirlenmesi

İlk user story'lerin çıkarılması

Wireframe ve logo tasarımının tamamlanması


 Tamamlananlar:

Görev	Durum	Açıklama

Proje vizyon dokümanı oluşturuldu		Eğitim temasına uygunluk ve toplumsal katkı açıklandı
Takım rolleri netleşti	
Herkesin görevi belirlendi
User Story & Product Backlog oluşturuldu		Modlar ve senaryolar tanımlandı
Teknoloji altyapısı belirlendi	Streamlit, FastAPI, GPT-4 gibi
Wireframe ve sosyal medya görseli üretildi		Logo da dahil
Chatbot mantığı planlandı		Soru türlerine göre rehberlik/otomatik çıktı sunacak yapı netleşti



---

 Öne Çıkan User Story’ler

Kullanıcı İsteği	Ne Yapılacak	Katkısı

“Konu hakkında araştırma yapmak istiyorum”	AI destekli kaynak öneri akışı	Araştırma becerisi kazandırır
“Hazır bilgi istiyorum”	Web scraping + AI özetleme	Zaman kazandırır, öğrenmeye teşvik eder
“Harita ile gösterilsin”	Google Maps / StreetView API	Görsel destekle kavrayış güçlenir
“Çıktıyı PDF olarak alayım”	PDF modülü	Paylaşım ve arşivlemeye olanak tanır



---

 Kullanıcı Profilleri

 Üniversite öğrencileri

 Mahalle sakinleri

 STK çalışanları

 Eğitimciler

 Girişimci adayları



---

Öğrenme ve Teknik Gelişim Planı

Alan	Gelişime Açık Noktalar	Eylem

FastAPI	Backend geliştiriciler öğrenmeye başladı	Basit API endpoint’leri denenecek
LLM kullanımı	Prompt engineering üzerine çalışma yapılacak	LangChain / OpenAI kütüphanesi araştırılıyor
UI geliştirme	Wireframe hazır, frontend framework belirlenecek	Streamlit ile başlayıp React’e geçilebilir



---

 Bir Sonraki Sprint'te Hedeflenenler:

[ ] Basit chatbot arayüzü prototipi

[ ] İlk veri kaynağı bağlantısı (AFAD JSON, Google Maps)

[ ] Konu-seçim sistemi için butonlu yapı

[ ] Mod 1: “Kendi araştırmamı yapayım” akışının kurulması

[ ] Chatbotun etik kontrol senaryolarını örnekleme

[ ] Sprint sonunda 1 dakikalık demo video planı



---

 Görsel Çıktılar

 Logo & sosyal preview hazır

 Wireframe şeması üretildi

Chatbot açılış ekranı taslağı oluşturuldu (kategoriler: Bilgi Al / Araştır / Sorun Tespit Et / Ortak Fayda)


2.sprint

Daily Scrum (Haftalık Değerlendirme)
Gunluk iletişim ağırlıklı olarak WhatsApp üzerinden sağlanmıştır.
Hafta içinde ihtiyaca bagli olarak birkaç kez informal şekilde toplu değerlendirme toplantıları yapılmıştır.
Haftalik duzenli Google meet toplantilari yapilmistir.
Rollerde ihtiyaca gore paylasima gidilmesine karar verilmistir.
Fikrin genel akışı ve kullanıcı senaryoları için bir şema üzerinde uzlaşılmıştır.
Mekanik yazılım geliştirme süreci için başlangıç tarihi belirlenmiş, modül öncelikleri sıraya alınmıştır.
Proje fikrinin arastirma ve incelemelerle desteklenmesine karar verilmistir.
 Sprint Review
 Genel Amaç
Bu sprintte, MOD 1 ve MOD 2 için geliştirme öncesi hazırlıklar yapıldı. Teknik ihtiyaçlar, kullanıcı senaryoları ve temel bileşenler belirlendi. Hedef, bir sonraki sprintte fonksiyonel prototiplemeye hazır bir zemin oluşturmaktı. Grup isleyisinin etkinliginin ve verimliginin artmasi icin iyilestirmeler yapilmasi planlandi.


MOD 1 – Rehberlik Eden Asistan (Kullanıcının kendi araştırmasını yaptığı senaryo)
Sprintte Yapılanlar:
Kullanıcının arama sürecini nasıl adım adım yönlendireceği taslaklandı.
Arayüzde yer alacak: “soru girme”, “konu tanıma”, “kaynak önerisi” bileşenleri belirlendi,.
Backlog’a eklenecek modül: Anahtar kelime sınıflandırıcısı + kaynak eşleştirme algoritması.
Grup ici gorev dagilimlari ve is takibi iyilestirmesi yapildi.
Planlanan Yapı:
Girdi ekranı → Konu sınıflandırması → Kaynak listesi → Araştırma adımları
Eğitim odaklı, öğretici içeriklerle desteklenecek rehber akışı


 MOD 2 – Otomatik Bilgi Toplayıcı Asistan (Hazır çıktı isteyen kullanıcı)
Sprintte Yapılanlar:
Hazır bilgi isteyen kullanıcı için minimum veri akışı kurgulandı
Kullanılacak API ve veri kaynakları listelendi (AFAD, Google Maps, E-Devlet açık veri setleri vb.)
Veri çekme → sadeleştirme → raporlama adımları belirlendi
Planlanan Yapı:
Sorgu ekranı → Web scraping/API → Etik kontrol → Sonuç ekranı (PDF / harita ile destekli)
Gerektiğinde coğrafi görselleştirme ve çıktı alma modülü ile entegre çalışacak
Sprint Sonuçları & Geri Bildirimler
Tamamlanan Hazırlıklar
 - MOD 1 ve MOD 2'nin kullanıcı hikâyeleri netleştirildi
 - Teknik gereksinim listesi çıkarıldı (API, LLM, filtreleme, çıktı alma)
 -  Geliştirme süreci için önceliklendirme listesi hazırlandı
Elde Edilen Geri Bildirimler:
MOD 1'in özellikle eğitsel yönü öne çıkarılmalı (pop-up, bilgi kutusu önerisi)
MOD 2’nin sorgu sonrası ekranında sade ve net bir çıktı beklentisi var
Geliştirme öncesi kullanıcı test senaryoları hazırlanmalı

 Sonraki Sprint’e Aktarılanlar
Kullanıcı arayüz prototipinin oluşturulması
MOD 1 için konu–kaynak eşleştirme modülünün MVP’sine başlanması
MOD 2 için ilk veri çekme testlerinin yapılması
Etik kontrol mekanizmasının temel kurallarının backend'e entegre edilmesi
EKLER ve Ekran Görüntüleri
Aşağıda, “OSINT for Daily Life” projesine ilişkin örnek uygulama ekran görüntüleri yer almaktadır:










