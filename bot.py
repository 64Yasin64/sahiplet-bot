import requests
import time
import schedule
from bs4 import BeautifulSoup

BOT_TOKEN = "8505598275:AAE-tixbmUMiRByNI2Ui2bWJ7LhI8g2Dr_4"
CHAT_ID = "7020744731"

URUNLER = [
    "GTX 1060 6GB",
    "RX 580 8GB"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

OLUMLU = ["kusursuz", "sorunsuz", "hatasız"]
OLUMSUZ = ["arızalı", "tamir", "mining", "bozuk"]

def sahibinden_ara(urun):
    url = f"https://www.sahibinden.com/arama?query_text={urun.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    ilanlar = []

    for ilan in soup.select(".searchResultsItem"):
        try:
            baslik = ilan.select_one(".classifiedTitle").text.strip()
            fiyat = ilan.select_one(".searchResultsPriceValue").text.strip()
            link = "https://www.sahibinden.com" + ilan.select_one("a")["href"]

            metin = baslik.lower()

            if any(k in metin for k in OLUMLU) and not any(k in metin for k in OLUMSUZ):
                ilanlar.append((fiyat, baslik, link))
        except:
            continue

    return ilanlar

def bildir():
    for urun in URUNLER:
        ilanlar = sahibinden_ara(urun)

        if not ilanlar:
            continue

        mesaj = f"🔥 SAHİBİNDEN UYGUN İLANLAR\n\n📦 {urun}\n\n"

        for i, ilan in enumerate(ilanlar[:5], 1):
            mesaj += f"{i}) 💰 {ilan[0]}\n{ilan[1]}\n🔗 {ilan[2]}\n\n"

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": mesaj
            }
        )

schedule.every().day.at("07:00").do(bildir)

while True:
    schedule.run_pending()
    time.sleep(60)
