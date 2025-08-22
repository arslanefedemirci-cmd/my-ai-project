# Gerekli kütüphaneleri içeri aktarıyoruz
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import random

# --- FONKSİYONLAR ---

# Ansiklopedi Modu: İnternetten bilgi çeker ve özetler
def ansiklopedi_modu(konu):
    url_konu = konu.replace(" ", "_")
    site_adresi = f"https://tr.wikipedia.org/wiki/{url_konu}"
    try:
        istek = requests.get(site_adresi)
        istek.raise_for_status()
        soup = BeautifulSoup(istek.text, 'html.parser')
        paragraflar = soup.find_all('p')
        ham_metin = "".join([p.text for p in paragraflar[:3]])
        temiz_metin = re.sub(r'\[\d+\]', '', ham_metin)
        cumleler = temiz_metin.split('. ')
        ozet = ' '.join(cumleler[:2]) + '.'
        return ozet
    except requests.exceptions.HTTPError as errh:
        return f"Hata: '{konu}' konusu bulunamadı. ({errh})"
    except Exception as e:
        return f"Bir hata oluştu: {e}"

# Kanka Modu: Kullanıcıyla sohbet eder
def kanka_modu(kullanici_mesaji, ana_komut):
    mesaj = kullanici_mesaji.lower()
    
    if ana_komut in ["ansiklopedi", "plan", "araştırma"]:
        return "Bilgi talebini aldım. Bu konu hakkında daha resmi bir dilde yardımcı olabilirim."

    olumlu_kelimeler = ["mutlu", "harika", "sevindim", "iyi", "süper", "mükemmel"]
    olumsuz_kelimeler = ["üzgün", "kötü", "morali bozuk", "berbat", "hayal kırıklığı"]
    
    olumlu_sayi = sum(1 for kelime in olumlu_kelimeler if kelime in mesaj)
    olumsuz_sayi = sum(1 for kelime in olumsuz_kelimeler if kelime in mesaj)
    
    if olumlu_sayi > olumsuz_sayi:
        return "Pozitif enerji hissediyorum! Ne bu coşku? 😄"
    elif olumsuz_sayi > olumsuz_sayi:
        return "Sana bir sarılma borçluyum. Her şey düzelecek. 😔"
    elif "nasılsın" in mesaj:
        return "İyiyim reis, sen nasılsın? 😊"
    elif "merhaba" in mesaj or "selam" in mesaj:
        return "Aleykümselam. Nasılsın? 👋"
    else:
        return "Ne demek istedin tam anlamadım. Başka bir şey söyle? 🤔"

# Üretim Modu: Yaratıcı cümleler oluşturur
def uretim_modu(kelimeler):
    if len(kelimeler) < 2:
        return "Lütfen en az iki kelime girin."
    random.shuffle(kelimeler)
    olumlu_kelimeler = ["huzurlu", "parlak", "gizli", "sonsuz", "coşkulu", "parıltılı"]
    secilen_olumlu_kelime = random.choice(olumlu_kelimeler)
    uretilen_metin = f"Bir {kelimeler[0]} {secilen_olumlu_kelime} bir {kelimeler[1]} yarattı."
    return uretilen_metin

# Planlama Modu: Bilgiyi adım adım plana dönüştürür
def planlama_modu(konu):
    bilgi = ansiklopedi_modu(konu)
    if bilgi.startswith("Hata:"):
        return bilgi
    adımlar = [c.strip() for c in bilgi.split('. ') if c.strip()]
    plan = "İşte " + konu.capitalize() + " için basit bir plan:\n"
    for i, adim in enumerate(adımlar):
        plan += f"{i+1}. Adım: {adim}.\n"
    return plan

# Şaka Modu: Rastgele bir şaka döner
def saka_modu():
    sakalar = [
        "Temel bir gün uçağa biner ve pilotu yanına çağırır: 'Pilot bey, siz hiç havada uçağın motoru durdu mu?' diye sorar. Pilot, 'Hayır, hiç motor durmadı.' diye cevap verir. Temel, 'İyi, o zaman siz bu uçağı kullanamazsınız çünkü ben motoru durdurdum.' der.",
        "Öğretmen, Temel'e: 'İki tane sıfır yaz bakalım.' der. Temel, iki tane sıfır yazar. Öğretmen: 'Bunları nasıl okursun?' diye sorar. Temel: 'Hiç biri.' diye cevap verir.",
        "Sorumluluk sahibi insanlar hep bir şeyler alırlar. Sorumsuzlar da hep boş boş dururlar.",
    ]
    return random.choice(sakalar)

# Araştırma Modu: Birden fazla konu hakkında bilgi çeker
def arastirma_modu(konular):
    sonuclar = ""
    for i, konu in enumerate(konular):
        bilgi = ansiklopedi_modu(konu)
        sonuclar += f"--- {i+1}. {konu.capitalize()} ---\n"
        sonuclar += f"{bilgi}\n\n"
    return sonuclar

# --- STREAMLIT ARAYÜZÜ ---

st.title("Yapay Zeka Asistanınız Hazalı")
st.write("Sizin için ne yapabilirim?")
st.write("Komutlar: `ansiklopedi`, `kanka`, `üretim`, `plan`, `şaka`, `araştırma`")

kullanici_girisi = st.text_input("Komutunuzu buraya girin:")

if st.button("Çalıştır"):
    komut_bolmeleri = kullanici_girisi.lower().split(" ", 1)
    ana_komut = komut_bolmeleri[0]
    
    if ana_komut in ["ansiklopedi", "ara"]:
        if len(komut_bolmeleri) > 1:
            bilgi = ansiklopedi_modu(komut_bolmeleri[1])
            st.write(f"### Bilgi:")
            st.write(bilgi)
        else:
            st.write("Lütfen bir konu belirtin.")
    elif ana_komut == "kanka":
        if len(komut_bolmeleri) > 1:
            cevap = kanka_modu(komut_bolmeleri[1], ana_komut)
            st.write(f"### Hazalı'nın Cevabı:")
            st.write(cevap)
        else:
            st.write("Lütfen bir şey söyle.")
    elif ana_komut == "üretim":
        if len(komut_bolmeleri) > 1:
            uretilen = uretim_modu(komut_bolmeleri[1].split())
            st.write(f"### Üretilen Metin:")
            st.write(uretilen)
        else:
            st.write("Lütfen en az iki kelime girin.")
    elif ana_komut == "plan":
        if len(komut_bolmeleri) > 1:
            plan = planlama_modu(konu)
            st.write(f"### Plan:")
            st.write(plan)
        else:
            st.write("Lütfen bir konu belirtin.")
    elif ana_komut == "şaka":
        saka = saka_modu()
        st.write(f"### Şaka:")
        st.write(saka)
    elif ana_komut == "araştırma":
        if len(komut_bolmeleri) > 1:
            konular = komut_bolmeleri[1].split()
            sonuclar = arastirma_modu(konular)
            st.write(f"### Araştırma Sonuçları:")
            st.write(sonuclar)
        else:
            st.write("Lütfen araştırmak istediğiniz konuları boşluk bırakarak yazın.")
    else:
        st.write("Bilinmeyen komut. Lütfen 'ansiklopedi', 'kanka', 'üretim', 'plan', 'şaka' veya 'araştırma' deneyin.")
