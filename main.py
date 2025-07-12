import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ---- Inställningar ----
KEYWORDS = ["rost", "obes", "felkod", "småfel", "små fel", "projekt", "besikt", "sliten", "motorfel"]
MAX_PRIS = 15000
BLOCKET_URL = f"https://www.blocket.se/annonser/hela_sverige/fordon/bilar?cg=1020&st=s&ps=0&pe={MAX_PRIS}"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def hitta_annons_urler():
    response = requests.get(BLOCKET_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    annonser = soup.find_all("a", href=True)
    
    matchningar = []

    for annons in annonser:
        text = annons.get_text().lower()
        url = "https://www.blocket.se" + annons["href"]
        if any(keyword in text for keyword in KEYWORDS):
            matchningar.append((text.strip(), url))

    return matchningar

def skicka_telegram_meddelande(meddelande):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": meddelande,
        "disable_web_page_preview": True,
    }
    requests.post(url, data=data)

if __name__ == "__main__":
    resultat = hitta_annons_urler()
    if resultat:
        for titel, url in resultat:
            meddelande = f"{titel}\n{url}"
            skicka_telegram_meddelande(meddelande)
    else:
        print("Inga matchande annonser hittades.")
